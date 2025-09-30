import threading
import time
import os

# Suprime los logs de gRPC que no son errores. Debe hacerse antes de importar librerías de Google.
os.environ['GRPC_VERBOSITY'] = 'ERROR'

from dotenv import load_dotenv

load_dotenv()

os.system('cls' if os.name == 'nt' else 'clear')

try:
    from . import engine, clean, tts
    from .chat import ChatManager # Importamos la clase específica
    from .context import ContextManager
except ImportError:
    import clean
    import engine
    import tts
    from chat import ChatManager
    from context import ContextManager
except RuntimeError as e:
    print(f"No se pudo iniciar la aplicación: {e}")
    exit()

class AppState:
    """Maneja el estado de ejecución de forma segura entre hilos."""
    def __init__(self):
        self.is_running = False
        self.lock = threading.Lock()

    def start(self):
        with self.lock:
            self.is_running = True

    def stop(self):
        with self.lock:
            self.is_running = False

    def get_status(self):
        with self.lock:
            return self.is_running

class VTCore:
    def __init__(self, log_callback=None):
        """
        Inicializa el núcleo de la lógica del VTuber.
        :param log_callback: Una función opcional para enviar mensajes de log al exterior.
        """
        self.app_state = AppState()
        self.chat_thread = None
        self.log = log_callback if log_callback else print

        # VTCore ahora tiene un gestor de contexto dedicado
        self.context_manager = ContextManager(log_callback=self.log)
        system_prompt = self.context_manager.create_system_prompt()

        self.log(f"[VTCore] Prompt de sistema generado:\n---INICIO PROMPT---\n{system_prompt}\n---FIN PROMPT---")
        self.speak_text = tts.speak_text # Asignamos la función de tts
        self.model = engine.init_model(system_prompt)

    def start_chat_processing(self, chat_manager: ChatManager):
        """Inicia el procesamiento del chat en un hilo separado."""
        if self.app_state.get_status():
            self.log("El proceso ya está en ejecución.")
            return

        self.app_state.start()
        self.chat_thread = threading.Thread(target=self.process_chat, args=(chat_manager,))
        self.chat_thread.start()

        # Inicia una nueva sesión de chat con memoria en el ContextManager
        self.context_manager.start_chat_session(self.model)

    def stop(self, chat_manager: ChatManager):
        """Detiene de forma segura el procesamiento del chat."""
        if self.app_state.get_status():
            self.log("Iniciando secuencia de apagado...")
            self.app_state.stop()
            chat_manager.stop() # Llama al nuevo método stop del ChatManager

    def process_chat(self, chat_manager: ChatManager):
        """Descarga y procesa los mensajes del chat de YouTube."""
        self.log("Iniciando ciclo de procesamiento de chat.")
        try:
            # El core ahora solo pide mensajes al ChatManager
            for message_data in chat_manager.get_messages():
                if not self.app_state.get_status(): # Permite detener el bucle
                    self.log("Deteniendo el procesamiento de chat.")
                    break

                author = message_data.get('author', 'Desconocido')
                message = message_data.get('message', '')
                self.log(f"[CHAT] {author}: {message}")

                # 1. Comprobar si el mensaje activa una regla predefinida
                rule_response = self.context_manager.check_rules(message)

                if rule_response:
                    response_text = rule_response
                    self.log(f"[ELY] {response_text}")
                    self.speak_text(response_text)
                else:
                    # 2. Si no hay regla, generar respuesta con Gemini.
                    # La respuesta es un generador que produce trozos de texto.
                    response_generator = engine.generate_response_with_history(
                        self.context_manager.chat_session,
                        f"{author} dice: {message}"
                    )
                    
                    # 3. Ensamblar la respuesta completa del generador.
                    #    Podemos seguir mostrando los trozos en la consola para un efecto "en vivo".
                    full_response = ""
                    
                    # Consumimos el generador y procesamos cada chunk
                    for chunk in response_generator:
                        cleaned_chunk = clean.clean_text(chunk)
                        self.log(f"[ELY_CHUNK] {cleaned_chunk}")
                        full_response += cleaned_chunk

                    # 4. Una vez ensamblada, verbalizar la respuesta completa para un audio fluido.
                    self.log(f"[ELY] {full_response}")
                    if full_response.strip():  # Solo hablar si hay contenido
                        # self.log(f"[DEBUG] Enviando a TTS: {len(full_response)} caracteres")
                        self.speak_text(full_response)
                    # else:
                    #     self.log("[DEBUG] Respuesta vacía, no se envía a TTS")
        except Exception as e:
            self.log(f"Error durante el procesamiento del chat: {e}")
        finally:
            self.log("El procesamiento de chat ha finalizado.")
            self.app_state.stop()

if __name__ == '__main__':
    # --- Bloque para testear la lógica completa de VTCore ---
    # Simula el comportamiento de la aplicación principal al procesar un chat en vivo.
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- Iniciando Live Ely Vtuber) ---")
    print("Presiona Ctrl+C para detener la simulación.\n")

    def custom_test_logger(log_message: str):
        """Filtra y formatea los logs para una visualización limpia del chat."""
        if log_message.startswith('[CHAT]'):
            print(log_message.replace('[CHAT] ', ''), end='\n\n')
        elif log_message.startswith('[ELY]'):
            # El \r asegura que la línea se sobrescriba, eliminando los trozos anteriores.
            # El espacio al final limpia cualquier carácter residual si la nueva línea es más corta.
            print(f"\r{log_message.replace('[ELY] ', 'Ely Vtuber: ')} ", end='\n\n')
        elif log_message.startswith('[ELY_CHUNK]'):
            # Imprime los trozos a medida que llegan para una sensación de "estar escribiendo".
            # El \r al final hace que el cursor vuelva al inicio de la línea.
            print(f"\rEly Vtuber: {log_message.replace('[ELY_CHUNK] ', '')}", end='')
        # elif log_message.startswith('[DEBUG]') or log_message.startswith('[TTS'):
        #     # Mostrar logs de debug y TTS para diagnóstico
        #     print(f"\n{log_message}")

    # Instanciamos el VTCore para usar toda la lógica de la aplicación.
    # Pasamos el logger personalizado para mostrar el chat en el formato deseado.
    core_instance = VTCore(log_callback=custom_test_logger)

    # 1. Pedimos la URL del directo y creamos el ChatManager.
    try:
        live_url = input("Pega la URL del directo de YouTube: ")
        chat_manager = ChatManager(live_url)

        if chat_manager.is_connected():
            # 2. Pasamos el gestor de chat (no la URL) al core para que inicie el proceso.
            core_instance.start_chat_processing(chat_manager)
            # Bucle principal para mantener la aplicación viva mientras el hilo de chat funciona.
            while core_instance.app_state.get_status():
                time.sleep(1)
        else:
            # Este mensaje se mostrará si ChatManager no pudo inicializarse (p.ej. URL inválida)
            print("\nNo se pudo conectar al chat. Verifica la URL o que el directo esté activo.")

    except KeyboardInterrupt:
        print("\nFinalizando live Ely Vtuber...")
        # Usamos el nuevo método stop para un apagado limpio
        core_instance.stop(chat_manager)
        if core_instance.chat_thread:
            core_instance.chat_thread.join()
        print("Recursos liberados.")
    print("Live Finalizado.")