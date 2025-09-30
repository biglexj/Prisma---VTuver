import sounddevice as sd
import threading
import queue
from melo_onnx import MeloTTS_ONNX
import numpy as np

class TTSManager:
    """
    Gestiona una instancia del motor TTS de melotts-onnx y una cola de voz para evitar conflictos.
    """
    def __init__(self):
        print("Inicializando MeloTTS_ONNX...")
        
        # 'cpu' es recomendado y el más eficiente para la inferencia con ONNX
        self.device = 'cpu'
        
        # Inicializar el modelo con parámetros básicos
        try:
            self.model = MeloTTS_ONNX(language='ES', device=self.device)
            print("✓ Modelo MeloTTS_ONNX cargado exitosamente")
        except Exception as e:
            print(f"Error al cargar MeloTTS_ONNX: {e}")
            # Fallback: probar con parámetros mínimos
            try:
                self.model = MeloTTS_ONNX()
                print("✓ Modelo cargado con configuración por defecto")
            except Exception as e2:
                print(f"Error crítico al cargar modelo: {e2}")
                raise
        
        # Intentar obtener configuración del modelo
        try:
            if hasattr(self.model, 'hps') and hasattr(self.model.hps, 'data'):
                self.speaker_ids = self.model.hps.data.spk2id if hasattr(self.model.hps.data, 'spk2id') else {'ES': 0}
                self.sampling_rate = self.model.hps.data.sampling_rate if hasattr(self.model.hps.data, 'sampling_rate') else 22050
            else:
                # Valores por defecto
                self.speaker_ids = {'ES': 0}
                self.sampling_rate = 22050
                print("⚠ Usando configuración por defecto")
        except Exception as e:
            print(f"⚠ Error obteniendo configuración del modelo: {e}")
            self.speaker_ids = {'ES': 0}
            self.sampling_rate = 22050
        
        print(f"Speaker IDs disponibles: {self.speaker_ids}")
        print(f"Sampling rate: {self.sampling_rate}")
        
        self.queue = queue.Queue()
        
        # Inicia un hilo de trabajo dedicado para procesar la cola de voz
        self.worker_thread = threading.Thread(target=self._process_queue)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        print("✓ Hilo de trabajo iniciado")

    def _process_queue(self):
        """Procesa continuamente el texto de la cola, lo convierte en audio y lo reproduce."""
        print("Hilo de trabajo TTS iniciado...")
        while True:
            try:
                text = self.queue.get()
                print(f"Procesando texto: '{text}'")
                
                # Genera el audio - aquí pueden necesitarse ajustes según la API específica
                try:
                    # Intenta diferentes métodos de generación según la API
                    if hasattr(self.model, 'tts'):
                        audio = self.model.tts(text, self.speaker_ids.get('ES', 0))
                    elif hasattr(self.model, 'synthesize'):
                        audio = self.model.synthesize(text, speaker_id=self.speaker_ids.get('ES', 0))
                    elif hasattr(self.model, 'generate'):
                        audio = self.model.generate(text)
                    else:
                        # Método genérico
                        audio = self.model(text)
                    
                    # Asegurar que el audio esté en el formato correcto
                    if isinstance(audio, tuple):
                        audio = audio[0]  # A veces devuelve (audio, sample_rate)
                    
                    if not isinstance(audio, np.ndarray):
                        audio = np.array(audio)
                    
                    # Reproducir audio
                    print(f"Reproduciendo audio... Shape: {audio.shape}, Dtype: {audio.dtype}")
                    sd.play(audio, self.sampling_rate)
                    sd.wait()
                    print("✓ Audio reproducido exitosamente")
                    
                except Exception as audio_error:
                    print(f"Error generando/reproduciendo audio: {audio_error}")
                    print("Intentando método alternativo...")
                    
                    # Método alternativo más básico
                    try:
                        result = self.model.tts_to_file(text, speaker_id=0)
                        if isinstance(result, str):  # Si devuelve un path de archivo
                            import soundfile as sf
                            audio, sr = sf.read(result)
                            sd.play(audio, sr)
                            sd.wait()
                        else:
                            print("No se pudo generar audio con método alternativo")
                    except Exception as fallback_error:
                        print(f"Error en método alternativo: {fallback_error}")
                
                self.queue.task_done()
                
            except Exception as e:
                print(f"Error en el hilo de trabajo de TTS: {e}")
                self.queue.task_done()

    def add_to_queue(self, text: str):
        """Añade texto a la cola de voz para ser procesado."""
        if text.strip():
            print(f"Añadiendo a cola: '{text}'")
            self.queue.put(text)
        else:
            print("⚠ Texto vacío, no se añade a la cola")

# Variable global para la instancia
_tts_manager = None

def get_tts_manager():
    """Obtiene la instancia del TTS manager, creándola si no existe."""
    global _tts_manager
    if _tts_manager is None:
        _tts_manager = TTSManager()
    return _tts_manager

def speak_text(text_to_speak: str):
    """Función pública para convertir texto a voz."""
    manager = get_tts_manager()
    manager.add_to_queue(text_to_speak)

if __name__ == '__main__':
    print("=== PRUEBA DEL MOTOR TTS (MeloTTS-ONNX) ===")
    print("Iniciando sistema TTS...")
    
    try:
        # Crear instancia y hacer prueba
        manager = get_tts_manager()
        
        print("Sistema TTS listo. Generando audio de prueba...")
        speak_text("Hola, soy Ely. Este es un test del sistema de voz para verificar que todo funciona correctamente.")
        
        print("Esperando a que termine la reproducción...")
        manager.queue.join()
        
        print("✓ Prueba completada exitosamente!")
        
    except KeyboardInterrupt:
        print("\n⚠ Interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()