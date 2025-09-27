import ollama as ollama  # Se usa en la función ollama_engine
from chat_downloader import ChatDownloader  # Se usa en la función main para obtener el chat de YouTube
import pyttsx3  # Se usa en la función speak para la síntesis de voz
from rapidfuzz import process  # Se usa en la función rule_resultado para encontrar coincidencias
import random  # Se usa en la función rule_resultado para elegir respuestas aleatorias
import json  # Se usa para cargar los archivos JSON con la personalidad y reglas de Ely
import re  # Se usa para filtrar el texto generado por Ollama

# Cargar el JSON con la rule
with open("context/json/ely_personality.json", "r", encoding="utf-8") as archivo:
    ely_personality = json.load(archivo)

with open("context/json/ely_rules.json", "r", encoding="utf-8") as file:
    ely_rules = json.load(file)

ely_personality_text = (
    "Nombre: " + ely_personality["nombre"] + "\n" +
    "Personalidad: " + ely_personality["personalidad"] + "\n" +
    "Estilo Visual: " + ely_personality["estilo_visual"] + "\n" +
    "Interacciones: " + ely_personality["interacciones"] + "\n" +
    "Habilidades: " + ely_personality["habilidades"] + "\n" +
    "Tono de voz: " + ely_personality["tono_de_voz"] + "\n" +
    "Misión: " + ely_personality["mision"] + "\n" +
    "Bienvenida: " + ely_personality["bienvenida"] + "\n" +
    "Despedida: " + ely_personality["despedida"] + "\n" +
    "Humor: " + ely_personality["humor"]
)

# Función para buscar una respuesta
def rule_resultado(chat_YT):
    for clave, valor in ely_rules.items():
        if "pregunta" in valor:
            match = process.extractOne(chat_YT, valor["pregunta"])
            if match and match[1] > 80:
                if "respuesta_1" in valor:
                    return random.choice([valor["respuesta_1"], valor["respuesta_2"]])
                return valor["respuesta"]
    return "Toma un criterio neutral a las preguntas con un poco de sarcasmo de vez en cuando."

# Función para la síntesis de voz con pyttsx3
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"✗ Error al reproducir el texto: {e}")

contexto = []
def agregar_contexto(texto):
    if len(contexto) > 10:  # Limitar la memoria
        contexto.pop(0)
    contexto.append(texto)

def obtener_contexto():
    return " ".join(contexto)

# Definir la función principal para el chat
def main():
    url = "https://www.youtube.com/watch?v=8_vRfMXWl98&t=444s"
    chat = ChatDownloader().get_chat(url)

    if chat:
        for chat_YT in chat:
            message = chat_YT.get('message', '')
            author_name = chat_YT.get('author', {}).get('name', 'Desconocido')

            if message:
                chat_text = author_name + ": " + message
                print(chat_text)
                resultado = rule_resultado(message)
                response = ollama_engine(chat_text, ely_personality_text, resultado)

                if response:
                    filtered_text = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
                    print("Ely VTuber:", filtered_text)
                    speak(filtered_text)

# Función para obtener la respuesta de Ollama
def ollama_engine(chat_text, personality_text, rule_resultado):
    prompt = (
        f"Tu personalidad es la siguiente: {personality_text}\n"
        f"La pregunta que te hacen es: {chat_text}\n"
        f"Tener en cuenta ciertos mensajes y tomar con cautela: {rule_resultado}\n"
        f"Tu respuesta debe ser breve, concisa y acorde a tu personalidad.\n"
        f"Evita decir te ayudare en algo, porque eres una VTuber y enfocada en la interacción con el público del live."
    )
    
    try:
        response = ollama.chat(
            model="deepseek-r1:1.5b",
            messages=[{"role": "user", "content": prompt}]
        )
        generated_text = response["message"]["content"]
        filtered_text = re.sub(r'<think>.*?</think>', '', generated_text, flags=re.DOTALL).strip()
        return filtered_text
    except Exception as e:
        print(f"✗ Error getting Ollama response: {e}")
        return None

if __name__ == "__main__":
    main()