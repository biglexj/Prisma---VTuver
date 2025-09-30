# 🎤 Ely VTuber - AI-Powered Virtual Streamer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Gemini AI](https://img.shields.io/badge/Powered%20by-Gemini%20AI-blueviolet.svg)](https://ai.google.dev/)
[![YouTube](https://img.shields.io/badge/YouTube-Live%20Chat-red.svg)](https://youtube.com)

VTuber con inteligencia artificial que interactúa en tiempo real con el chat de YouTube Live usando Google Gemini API.

## 📜 Descripción

Ely VTuber es una aplicación que permite crear una VTuber con IA capaz de:
- 📺 Conectarse a transmisiones en vivo de YouTube
- 💬 Leer y responder mensajes del chat en tiempo real
- 🧠 Generar respuestas inteligentes usando Google Gemini AI
- 🗣️ Convertir las respuestas a voz (TTS)
- 🎭 Mantener un contexto conversacional con memoria de chat
- ⚡ Procesar múltiples mensajes de forma eficiente

Perfecto para streamers que quieren agregar un co-host con IA o crear contenido interactivo automatizado.

## ✨ Características Principales

*   **🤖 IA Conversacional** - Usa Google Gemini para respuestas naturales y contextuales
*   **📡 Chat en Tiempo Real** - Se conecta directamente al chat de YouTube Live
*   **🎯 Sistema de Reglas** - Respuestas predefinidas para comandos específicos
*   **💾 Gestión de Contexto** - Mantiene el historial de conversación para respuestas coherentes
*   **🔊 Text-to-Speech** - Convierte las respuestas a voz
*   **🧵 Procesamiento Multihilo** - Maneja el chat sin bloquear la aplicación
*   **🛡️ Manejo Seguro de Estado** - Control thread-safe del ciclo de vida

## 🛠️ Tech Stack

**Core:**
- Python 3.11+
- Google Gemini AI API
- pytchat (YouTube Live Chat)

**Procesamiento:**
- Threading (procesamiento paralelo)
- dotenv (gestión de variables de entorno)

**TTS & Context:**
- Text-to-Speech engine personalizado
- Context Manager para memoria de chat

## 🚀 Empezando

### ✅ Prerrequisitos

*   [Python](https://www.python.org/) 3.8 o superior
*   Una API Key de Google Gemini ([Obtener aquí](https://ai.google.dev/))
*   pip (gestor de paquetes de Python)

### ⚙️ Instalación

1.  **Clona el repositorio:**
    ```sh
    git clone https://github.com/biglexj/Prisma---VTuver.git
    cd Prisma---VTuver
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

4.  **Configura las variables de entorno:**
    
    Crea un archivo `.env` en la raíz del proyecto:
    ```env
    GEMINI_API_KEY="tu_api_key_de_gemini_aqui"
    GRPC_VERBOSITY="ERROR"
    ```

## 🎮 Uso

### Modo Básico

```sh
python -m vtcore
```

La aplicación te pedirá la URL del directo de YouTube:
```
Pega la URL del directo de YouTube: https://www.youtube.com/watch?v=xxxxx
```

### Integración en tu Código

```python
from vtcore import VTCore
from chat import ChatManager

# Inicializa el core con un logger personalizado (opcional)
def my_logger(message):
    print(f"[LOG] {message}")

core = VTCore(log_callback=my_logger)

# Conecta al chat de YouTube
live_url = "https://www.youtube.com/watch?v=xxxxx"
chat_manager = ChatManager(live_url)

# Inicia el procesamiento
if chat_manager.is_connected():
    core.start_chat_processing(chat_manager)
    
    # Tu lógica aquí...
    
    # Detener de forma segura
    core.stop(chat_manager)
```

### Estructura de Módulos

```python
vtcore/
├── __init__.py       # Núcleo principal (VTCore)
├── engine.py         # Integración con Gemini AI
├── chat.py           # Gestión del chat de YouTube
├── context.py        # Manejo de contexto y memoria
├── tts.py            # Text-to-Speech
└── clean.py          # Limpieza de texto
```

## 📋 Componentes Principales

### VTCore
Núcleo principal que orquesta todos los componentes:
```python
core = VTCore(log_callback=print)
core.start_chat_processing(chat_manager)
```

### ChatManager
Gestiona la conexión con YouTube Live:
```python
chat_manager = ChatManager(youtube_url)
for message in chat_manager.get_messages():
    print(message['author'], message['message'])
```

### ContextManager
Mantiene el historial y contexto de la conversación:
```python
context = ContextManager()
system_prompt = context.create_system_prompt()
context.start_chat_session(model)
```

## 🔧 Configuración Avanzada

### Sistema de Reglas Predefinidas

Puedes agregar respuestas automáticas para comandos específicos en el `ContextManager`:

```python
def check_rules(self, message):
    if "!comandos" in message.lower():
        return "Comandos disponibles: !hola, !info, !comandos"
    return None
```

### Personalizar el Prompt del Sistema

Modifica el método `create_system_prompt()` en `context.py` para cambiar la personalidad de tu VTuber.

### Ajustar el TTS

El módulo `tts.py` puede ser reemplazado con tu engine de TTS preferido (Google TTS, Azure TTS, ElevenLabs, etc.)

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si quieres mejorar Ely VTuber:

1.  Haz un **Fork** del proyecto
2.  Crea una rama (`git checkout -b feature/mejora-increible`)
3.  Commit tus cambios (`git commit -m 'Add: mejora increíble'`)
4.  Push a la rama (`git push origin feature/mejora-increible`)
5.  Abre un **Pull Request**

### Ideas para Contribuir

- 🎨 Diferentes personalidades para la VTuber
- 🔊 Soporte para más engines de TTS
- 📊 Sistema de métricas del chat
- 🎮 Integración con Twitch
- 💾 Persistencia de conversaciones
- 🌐 Soporte multilenguaje

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 📬 Contacto

**Biglex J** - [@biglexj](https://youtube.com/@biglexj)

**Repositorio:** [https://github.com/biglexj/Prisma---VTuver](https://github.com/biglexj/Prisma---VTuver)

**Website:** [biglexj.net.pe](https://biglexj.net.pe)

### Canales Relacionados
- [Biglex Dev](https://youtube.com/@biglexdev) - Contenido de desarrollo
- [Ely Vtuber](https://youtube.com/@ely_vtuber) - Canal oficial de la VTuber

## 🙏 Agradecimientos

*   [Google Gemini AI](https://ai.google.dev/) - Por la increíble API de IA
*   [pytchat](https://github.com/taizan-hokuto/pytchat) - Librería para YouTube Live Chat
*   La comunidad de VTubers y desarrolladores que inspiran este proyecto

## ⚠️ Notas Importantes

- Asegúrate de cumplir con los [Términos de Servicio de YouTube](https://www.youtube.com/t/terms)
- Respeta los límites de uso de la API de Gemini
- Este proyecto es con fines educativos y de entretenimiento

---

**Hecho con ❤️ y ☕ por [Biglex J](https://github.com/biglexj)**

*¡Dale ⭐ al repo si te gusta el proyecto!*