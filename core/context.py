import json
import random
from rapidfuzz import process

class ContextManager:
    """
    Gestiona la personalidad, las reglas y la memoria de la conversación.
    """
    def __init__(self, log_callback=print):
        self.log = log_callback
        # Corregimos las rutas para que coincidan con la estructura del proyecto
        self.personality = self._load_json("context/ely_personality.json")
        self.rules = self._load_json("context/rules.json")
        # El historial ahora se almacenará en un formato compatible con la API de Gemini
        self.chat_session = None

        # --- LOGS DE DEPURACIÓN ---
        if self.personality:
            self.log("[Context] Archivo de personalidad cargado correctamente.")
        else:
            self.log("[Context] ¡ADVERTENCIA! El archivo de personalidad está vacío o no se pudo cargar.")

        if self.rules:
            self.log("[Context] Archivo de reglas cargado correctamente.")
        else:
            self.log("[Context] ¡ADVERTENCIA! El archivo de reglas está vacío o no se pudo cargar.")

    def _load_json(self, file_path: str) -> dict:
        """Carga un archivo JSON de forma segura."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.log(f"Error crítico: No se pudo cargar '{file_path}'. Error: {e}")
            return {}

    def create_system_prompt(self) -> str:
        """Crea el prompt de sistema basado en la personalidad cargada."""
        if not self.personality:
            self.log("[Context] Usando prompt de sistema genérico porque la personalidad no está cargada.")
            return "Eres un asistente útil."
        
        return f"""
        Actúa como un VTuber con la siguiente personalidad:
        - Nombre: {self.personality.get('nombre', 'Ely')}
        - Personalidad: {self.personality.get('personalidad', '')}
        - Tono de voz: {self.personality.get('tono_de_voz', '')}
        - Misión: {self.personality.get('mision', '')}
        Responde a los mensajes del chat de forma concisa, amigable y enérgica, manteniendo siempre tu personaje.
        """

    def check_rules(self, message: str) -> str | None:
        """
        Comprueba si un mensaje coincide con alguna regla predefinida.
        Utiliza fuzzy matching para encontrar preguntas similares.
        """
        if not self.rules:
            return None

        for key, rule_data in self.rules.items():
            if "pregunta" in rule_data:
                # Compara el mensaje con la lista de preguntas de la regla
                match = process.extractOne(message, rule_data["pregunta"], score_cutoff=85)
                if match:
                    self.log(f"[Context] Regla '{key}' activada por coincidencia (Score: {match[1]:.0f}).")
                    # Si hay múltiples respuestas, elige una al azar
                    if "respuesta_1" in rule_data:
                        return random.choice([rule_data["respuesta_1"], rule_data["respuesta_2"]])
                    return rule_data["respuesta"]
        return None
    
    def start_chat_session(self, model):
        """
        Inicia una nueva sesión de chat con el modelo, que mantendrá el historial.
        """
        self.chat_session = model.start_chat(history=[])
        self.log("[Context] Nueva sesión de chat iniciada.")