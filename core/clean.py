import re

def clean_text(text: str) -> str:
    """
    Limpia un texto para que sea compatible con el motor TTS.

    Elimina:
    - Caracteres de formato como '*' y '#'.
    - Emojis y otros símbolos especiales.

    Conserva:
    - Letras (incluyendo tildes y 'ñ').
    - Números.
    - Espacios.
    """
    # 1. Elimina explícitamente los corchetes y otros caracteres problemáticos.
    text = re.sub(r'[\[\]\*#]', '', text)
    
    # Elimina cualquier caracter que no sea una letra (incluyendo acentos), número o espacio.
    # La expresión regular [^...] significa "cualquier caracter que NO esté en este conjunto".
    text = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s]', '', text)
    return text