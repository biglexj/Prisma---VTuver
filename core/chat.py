import pytchat
import time
from urllib.parse import urlparse, parse_qs
from collections import deque

class ChatManager:
    """Gestiona la conexión y obtención de mensajes del chat de YouTube."""

    def __init__(self, url: str):
        self.video_id = self._get_video_id(url)
        self._chat = None
        if self.video_id:
            print(f"[Chat] Conectando al stream de chat para el video ID: {self.video_id}...")
            self._chat = pytchat.create(video_id=self.video_id)
        else:
            print(f"[Chat] Error: URL de YouTube inválida: {url}")

    def is_connected(self) -> bool:
        """Verifica si la conexión al chat es válida."""
        return self._chat is not None and self._chat.is_alive()

    def get_messages(self):
        """Generador que produce mensajes del chat uno por uno."""
        if not self.is_connected():
            print("[Chat] No se pueden obtener mensajes, no hay conexión activa.")
            return

        while self.is_connected():
            for c in self._chat.get().items:
                yield {'author': c.author.name, 'message': c.message}
            time.sleep(1) # Pausa para no sobrecargar la API

    def stop(self):
        """Termina la conexión con el chat de YouTube."""
        if self._chat and self.is_connected():
            self.log("Desconectando del chat de YouTube...")
            self._chat.terminate()

    def _get_video_id(self, url: str) -> str | None:
        """Extrae el ID del video de una URL de YouTube."""
        parsed_url = urlparse(url)
        if parsed_url.hostname in ('youtu.be',):
            return parsed_url.path[1:]
        if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query).get('v', [None])[0]
            if parsed_url.path.startswith('/live/'):
                return parsed_url.path.split('/')[2]
        return None

if __name__ == '__main__':
    # --- Bloque para testear el módulo de chat de forma independiente ---
    live_url = input("Pega la URL del directo de YouTube: ")
    print(f"Iniciando test de chat para: {live_url}")
    print("Presiona Ctrl+C para detener.")
    chat_manager = ChatManager(live_url)
    if chat_manager.is_connected():
        try:
            for message in chat_manager.get_messages():
                print(f"[{message['author']}]: {message['message']}")
        except KeyboardInterrupt:
            print("\nTest de chat finalizado.")
