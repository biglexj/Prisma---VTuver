# Fix: Bloqueo de pyttsx3 en Threading (Windows)

## Problema

El sistema TTS solo leía el primer mensaje del chat y luego dejaba de funcionar. Los mensajes siguientes se agregaban a la cola pero nunca se reproducían.

### Síntomas
- ✅ El primer mensaje se reproducía correctamente
- ❌ Los mensajes subsecuentes no se reproducían
- ❌ El log `[TTS] Procesando: ...` aparecía pero nunca `[TTS] Completado`
- ❌ El worker thread del TTS se quedaba bloqueado indefinidamente

## Causa Raíz

**`pyttsx3.runAndWait()` se bloqueaba** después de la primera ejecución cuando se usaba en un thread daemon en Windows.

### Detalles técnicos:
1. `pyttsx3` en Windows usa **COM (Component Object Model)** para el TTS
2. COM tiene problemas conocidos con threading, especialmente en threads daemon
3. Una vez que `runAndWait()` se bloqueaba, el worker thread quedaba congelado
4. Los mensajes siguientes se encolaban pero nunca se procesaban porque el thread estaba bloqueado

### Código problemático:
```python
def _process_queue(self):
    while True:
        text = self.queue.get()
        self.engine.say(text)
        self.engine.runAndWait()  # ← Se bloqueaba aquí después del primer mensaje
        self.queue.task_done()
```

## Solución

Cambiar de **threading a subprocess** para ejecutar cada mensaje TTS en un proceso Python completamente separado.

### Implementación:
```python
def _speak_in_subprocess(self, text):
    """Ejecuta el TTS en un proceso separado para evitar bloqueos."""
    script = f"""
import pyttsx3
engine = pyttsx3.init()
engine.say({repr(text)})
engine.runAndWait()
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        timeout=30,  # Timeout de 30 segundos
        capture_output=True,
        text=True
    )
    return True
```

### Ventajas de esta solución:
- ✅ **Aislamiento total**: Cada mensaje tiene su propia instancia de `pyttsx3`
- ✅ **Sin conflictos de estado**: Los procesos no comparten memoria
- ✅ **Timeout automático**: Si un proceso se bloquea, se termina después de 30 segundos
- ✅ **Robustez**: Si un mensaje falla, no afecta a los siguientes

## Archivos Modificados

- **`core/tts.py`**: Implementación completa del sistema de subprocess
- **`core/core.py`**: Logs de debug para diagnóstico (luego comentados)

## Fecha

29/09/2025 - 18:35