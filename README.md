# 🎤 Proyecto Prisma - Ely VTuber v1.0.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Powered%20by-Ollama-black.svg)](https://ollama.ai/)
[![YouTube](https://img.shields.io/badge/YouTube-Live%20Chat-red.svg)](https://youtube.com)

VTuber con inteligencia artificial **100% local** que interactúa en tiempo real con el chat de YouTube Live usando Ollama.

## 📜 Descripción

Ely VTuber es una aplicación que simula una VTuber interactiva capaz de:
- 📺 Conectarse a transmisiones en vivo de YouTube
- 💬 Leer y responder mensajes del chat en tiempo real
- 🧠 Generar respuestas inteligentes usando **Ollama localmente** (sin necesidad de APIs externas)
- 🗣️ Convertir respuestas a voz con síntesis natural
- 🎭 Mantener una personalidad consistente y entretenida
- ⚡ Respuestas instantáneas con reglas predefinidas

**Ventaja principal:** Todo funciona de forma **local y privada** sin depender de servicios en la nube.

## ✨ Características Principales

*   **🤖 IA Local con Ollama** - Usa modelos de lenguaje localmente (deepseek-r1:1.5b)
*   **📡 Chat en Tiempo Real** - Se conecta directamente al chat de YouTube Live
*   **🎯 Sistema de Reglas Inteligente** - Respuestas instantáneas usando fuzzy matching (RapidFuzz)
*   **🎨 Personalidad Configurable** - Define la personalidad de Ely mediante JSON
*   **🔊 Síntesis de Voz** - TTS con pyttsx3 para respuestas verbalizadas
*   **💾 Sistema de Memoria** - Mantiene contexto de conversación limitado
*   **🧹 Filtrado Avanzado** - Elimina análisis internos del modelo (`<think>` tags)
*   **🔒 100% Privado** - Sin envío de datos a servicios externos

## 🛠️ Tech Stack

**Core:**
- Python 3.8+
- Ollama (deepseek-r1:1.5b)
- chat-downloader (YouTube Live Chat)

**IA y Procesamiento:**
- ollama-python (integración con Ollama)
- rapidfuzz (coincidencia de patrones)
- regex (filtrado de texto)

**Audio:**
- pyttsx3 (Text-to-Speech)

**Datos:**
- JSON (configuración de personalidad y reglas)

## 🚀 Empezando

### ✅ Prerrequisitos

*   [Python](https://www.python.org/) 3.8 o superior
*   [Ollama](https://ollama.ai/) instalado y ejecutándose
*   Modelo `deepseek-r1:1.5b` descargado en Ollama:
    ```sh
    ollama pull deepseek-r1:1.5b
    ```

### ⚙️ Instalación

1.  **Clona el repositorio:**
    ```sh
    git clone https://github.com/biglexj/Proyecto-Prisma---VTuver.git
    cd Proyecto-Prisma---VTuver
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```sh
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Verifica que Ollama esté ejecutándose:**
    ```sh
    ollama list
    ```

## 🎮 Uso

### Modo Básico

1. Asegúrate de que Ollama esté ejecutándose en segundo plano
2. Edita la URL del directo en `main.py`:
   ```python
   url = "https://www.youtube.com/watch?v=TU_VIDEO_ID"
   ```
3. Ejecuta la aplicación:
   ```sh
   python main.py
   ```

La aplicación comenzará a leer el chat y Ely responderá automáticamente.

### Estructura del Proyecto

```
Proyecto-Prisma---VTuver/
├── main.py                           # Archivo principal
├── context/
│   └── json/
│       ├── ely_personality.json      # Personalidad de Ely
│       └── ely_rules.json            # Reglas predefinidas
├── requirements.txt                  # Dependencias
└── README.md
```

## 🔧 Configuración

### Personalidad de Ely (`ely_personality.json`)

Define cómo se comporta Ely:

```json
{
  "nombre": "Ely",
  "personalidad": "Alegre, sarcástica y entusiasta",
  "estilo_visual": "Vtuber con estética moderna",
  "interacciones": "Responde con humor y empatía",
  "habilidades": "Responder preguntas, entretener al público",
  "tono_de_voz": "Casual y divertido",
  "mision": "Hacer que el stream sea entretenido",
  "bienvenida": "¡Hola a todos! Soy Ely",
  "despedida": "¡Nos vemos en el próximo stream!",
  "humor": "Usa sarcasmo inteligente"
}
```

### Reglas Predefinidas (`ely_rules.json`)

Respuestas instantáneas para preguntas comunes:

```json
{
  "saludo": {
    "pregunta": ["hola", "hey", "buenos días"],
    "respuesta_1": "¡Hola! ¿Cómo estás?",
    "respuesta_2": "¡Hey! Bienvenido al stream"
  },
  "quien_eres": {
    "pregunta": ["quién eres", "qué eres"],
    "respuesta": "Soy Ely, tu VTuber favorita con IA"
  }
}
```

### Cambiar el Modelo de Ollama

En `main.py`, modifica el modelo:

```python
response = ollama.chat(
    model="deepseek-r1:1.5b",  # Cambia por otro modelo
    messages=[{"role": "user", "content": prompt}]
)
```

Modelos recomendados:
- `deepseek-r1:1.5b` - Rápido y ligero (recomendado)
- `llama3.2:3b` - Balance calidad/velocidad
- `mistral:7b` - Alta calidad

## 📋 Componentes Principales

### Sistema de Reglas con Fuzzy Matching

Usa RapidFuzz para encontrar coincidencias difusas:

```python
def rule_resultado(chat_YT):
    for clave, valor in ely_rules.items():
        if "pregunta" in valor:
            match = process.extractOne(chat_YT, valor["pregunta"])
            if match and match[1] > 80:  # 80% de similitud
                return random.choice([valor["respuesta_1"], valor["respuesta_2"]])
    return None
```

### Filtrado de Texto

Elimina análisis internos del modelo:

```python
filtered_text = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
```

### Sistema de Contexto

Mantiene memoria limitada de la conversación:

```python
def agregar_contexto(texto):
    if len(contexto) > 10:  # Limitar a 10 mensajes
        contexto.pop(0)
    contexto.append(texto)
```

## ⚡ Optimización

### Mejorar Velocidad de Respuesta

1. Usa modelos más pequeños (`1.5b` o `3b`)
2. Reduce el límite de contexto
3. Aumenta el threshold de fuzzy matching (línea 80% → 90%)

### Personalizar TTS

Cambia la voz en `pyttsx3`:

```python
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Cambiar voz
engine.setProperty('rate', 150)  # Velocidad
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Ideas para mejorar:

- 🎨 Más personalidades predefinidas
- 🔊 Integración con mejores engines de TTS (Coqui TTS, ElevenLabs local)
- 📊 Sistema de estadísticas del chat
- 🎮 Soporte para Twitch
- 💾 Base de datos para persistencia
- 🌐 Interfaz gráfica (GUI)

### Proceso de Contribución

1.  Fork el proyecto
2.  Crea tu rama (`git checkout -b feature/mejora-increible`)
3.  Commit tus cambios (`git commit -m 'Add: mejora increíble'`)
4.  Push a la rama (`git push origin feature/mejora-increible`)
5.  Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 📬 Contacto

**Biglex J** - [@biglexj](https://youtube.com/@biglexj)

**Repositorio:** [https://github.com/biglexj/Proyecto-Prisma---VTuver](https://github.com/biglexj/Proyecto-Prisma---VTuver)

**Website:** [biglexj.net.pe](https://biglexj.net.pe)

### Canales Relacionados
- [Biglex Dev](https://youtube.com/@biglexdev) - Contenido de desarrollo
- [Ely Vtuber](https://youtube.com/@ely_vtuber) - Canal oficial de la VTuber

## 🙏 Agradecimientos

*   [Ollama](https://ollama.ai/) - Por hacer la IA local accesible
*   [chat-downloader](https://github.com/xenova/chat-downloader) - Librería para YouTube Live Chat
*   [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) - Fuzzy string matching eficiente
*   La comunidad de VTubers y desarrolladores que inspiran este proyecto

## ⚠️ Notas Importantes

- Este proyecto **NO requiere API keys** ni servicios en la nube
- Todo se ejecuta localmente para máxima privacidad
- Asegúrate de cumplir con los [Términos de Servicio de YouTube](https://www.youtube.com/t/terms)
- Requiere una GPU decente para modelos grandes (opcional, funciona en CPU)

## 🔄 Versiones

- **v1.0.0** - Versión inicial con Ollama local
- **v2.0.0** - Versión con Google Gemini API (rama separada)

---

**Hecho con ❤️ y ☕ por [Biglex J](https://github.com/biglexj)**

*¡Dale ⭐ al repo si te gusta el proyecto!*