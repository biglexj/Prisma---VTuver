import pyttsx3
import threading
import queue
import subprocess
import sys
import os

class TTSManager:
    """
    Manages a single TTS engine instance and a speech queue to prevent conflicts.
    """
    def __init__(self):
        self.queue = queue.Queue()
        self.use_subprocess = True  # Usar subprocess para evitar bloqueos
        
        # Start a dedicated worker thread to process the speech queue
        self.worker_thread = threading.Thread(target=self._process_queue)
        self.worker_thread.daemon = True  # Allows the main program to exit
        self.worker_thread.start()

    def _speak_in_subprocess(self, text):
        """Ejecuta el TTS en un proceso separado para evitar bloqueos."""
        try:
            # Crear un script temporal para ejecutar el TTS
            script = f"""
import pyttsx3
engine = pyttsx3.init()
engine.say({repr(text)})
engine.runAndWait()
"""
            # Ejecutar en un proceso separado con timeout
            result = subprocess.run(
                [sys.executable, "-c", script],
                timeout=30,  # Timeout de 30 segundos
                capture_output=True,
                text=True
            )
            return True
        except subprocess.TimeoutExpired:
            print(f"[TTS ERROR] Timeout al procesar el texto")
            return False
        except Exception as e:
            print(f"[TTS ERROR] Error en subprocess: {e}")
            return False

    def _process_queue(self):
        """Continuously processes text from the queue and speaks it."""
        while True:
            text = None
            try:
                text = self.queue.get()  # Blocks until an item is available
                if text:  # Solo procesar si hay texto
                    # print(f"[TTS] Procesando: {text[:50]}...")  # Log para debug
                    
                    if self.use_subprocess:
                        success = self._speak_in_subprocess(text)
                        # if success:
                        #     print(f"[TTS] Completado")
                        # else:
                        #     print(f"[TTS] Falló el procesamiento")
                    else:
                        # Fallback al método original
                        engine = pyttsx3.init()
                        engine.say(text)
                        engine.runAndWait()
                        print(f"[TTS] Completado")
            except Exception as e:
                print(f"[TTS ERROR] Error in TTS worker thread: {e}")
                import traceback
                traceback.print_exc()
            finally:
                # Siempre marcar la tarea como completada
                if text is not None:
                    self.queue.task_done()

    def add_to_queue(self, text: str):
        """Adds text to the speech queue."""
        self.queue.put(text)

# Create a single, shared instance of the TTS manager
_tts_manager = TTSManager()

def speak_text(text_to_speak: str):
    """
    Public function to add text to the speech queue.
    """
    # print(f"[TTS QUEUE] Agregando texto ({len(text_to_speak)} chars): {text_to_speak[:80]}...")
    _tts_manager.add_to_queue(text_to_speak)
