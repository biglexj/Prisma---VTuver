# main.py
import flet as ft

from core.chat import ChatManager
from core.core import VTCore
from interface.ui import AppUI
from interface.styles import APP_TITLE, START_BUTTON_STYLE, STOP_BUTTON_STYLE

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        # Pasamos el método de log de la UI al inicializar el Core.
        # Así, el Core puede enviar logs sin conocer la UI.
        self.core = VTCore(log_callback=self.log_to_ui)
        self.ui = AppUI(toggle_process_handler=self.toggle_process)

        self.init_ui()

    def init_ui(self):
        """Configura la página de Flet y añade la UI."""
        self.page.title = APP_TITLE
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.on_window_event = self.on_window_event
        
        self.page.add(self.ui.build_layout())
        self.page.update()

    def log_to_ui(self, message: str):
        """Añade un mensaje al log de la UI de forma segura entre hilos."""
        self.ui.log_view.value += message + "\n"
        self.page.update()

    def toggle_process(self, e):
        """Inicia o detiene el procesamiento del chat."""
        if not self.core.app_state.get_status():
            # Iniciar proceso
            url = self.ui.url_input.value
            if not url:
                self.log_to_ui("Error: Por favor, introduce una URL de YouTube.")
                return
            
            # Actualizamos la UI
            self.ui.start_button.text = "Detener Proceso"
            self.ui.start_button.style = STOP_BUTTON_STYLE
            self.page.update()

            # 1. Creamos el gestor de chat con la URL de la UI
            chat_manager = ChatManager(url)

            # 2. Verificamos la conexión y pasamos el gestor al core
            if chat_manager.is_connected():
                self.core.start_chat_processing(chat_manager)
            else:
                self.log_to_ui(f"Error: No se pudo conectar al chat de la URL proporcionada.")

        else:
            # Detener proceso
            self.core.app_state.stop() # El hilo se detendrá en la siguiente iteración
            self.log_to_ui("Solicitando detención del proceso...")
            self.ui.start_button.text = "Iniciar Proceso"
            self.ui.start_button.style = START_BUTTON_STYLE
        
        self.page.update()

    def on_window_event(self, e):
        if e.data == "close":
            self.core.app_state.stop()
            self.page.window_destroy()

def main(page: ft.Page):
    App(page)

if __name__ == "__main__":
    ft.app(target=main)