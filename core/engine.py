import google.generativeai as genai

# --- CONFIGURACIÓN DE GEMINI ---
try:
    # La librería buscará automáticamente la variable de entorno GOOGLE_API_KEY.
    genai.configure()
    # Verificamos que la clave fue encontrada listando los modelos.
    next(genai.list_models())
    print("API de Gemini configurada correctamente.")
except Exception as e:
    print(f"Error al configurar la API de Gemini. Asegúrate de que tu GOOGLE_API_KEY en el archivo .env es correcta. Error: {e}")
    # Lanzamos una excepción para detener la ejecución si la API es crucial.
    raise RuntimeError("Fallo en la configuración de la API de Gemini") from e

def init_model(system_prompt: str):
    """
    Inicializa y devuelve un GenerativeModel de Gemini con un prompt de sistema.
    """
    return genai.GenerativeModel(
        'gemini-flash-lite-latest',
        system_instruction=system_prompt
    )

def generate_response(model, user_message: str) -> str:
    """
    Genera una respuesta usando el modelo de Gemini.
    Devuelve el texto de la respuesta.
    """
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        print(f"Error al generar respuesta de Gemini: {e}")
        return "Lo siento, tuve un problema al procesar tu mensaje."

def generate_response_with_history(chat_session, user_message: str) -> str:
    """
    Genera una respuesta en modo streaming usando una sesión de chat que mantiene el historial.
    Devuelve un generador que produce los trozos (chunks) de la respuesta.
    """
    if not chat_session:
        # Si no hay sesión, devolvemos un generador vacío para mantener la consistencia.
        yield "Error: La sesión de chat no ha sido iniciada."
        return
    try:
        # Usamos stream=True para obtener un generador de trozos de respuesta.
        response_stream = chat_session.send_message(user_message, stream=True)
        for chunk in response_stream:
            yield chunk.text
    except Exception as e:
        print(f"Error al generar respuesta de Gemini con historial: {e}")
        yield "Ay, mi cerebro de IA tuvo un cortocircuito. ¿Puedes repetirlo?"