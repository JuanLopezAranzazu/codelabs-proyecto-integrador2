# Codelab Reconocimiento de voz con Python

## 1. ¿Qué librerías se usaron en el laboratorio para grabar y reconocer voz?

- **sounddevice**: para capturar y reproducir audio desde el micrófono.
- **scipy**: para procesar y manejar las señales de audio grabadas.
- **SpeechRecognition**: para convertir el audio grabado en texto.

## 2. ¿Por qué decidimos no usar PyAudio en esta práctica?

No usamos PyAudio porque suele generar problemas de instalación en macOS

## 3. ¿Qué rol cumple la función `recognize_google` en el código?

La función `recognize_google` se utiliza para enviar el audio grabado a la API de Google para su reconocimiento. Esta función toma el audio en formato WAV y devuelve el texto transcrito.

## 4. ¿Qué ocurre si `SpeechRecognition` no entiende lo que dijiste?

Si `SpeechRecognition` no entiende lo que dijiste, lanzará una excepción `UnknownValueError`. En el código, esto se maneja mostrando un mensaje de error y pidiendo al usuario que repita la frase.

## 5. ¿Cómo se guardó temporalmente el archivo WAV en el código?

El archivo de audio se guardó de forma temporal usando el módulo `tempfile`, que genera un nombre de archivo único con la extensión `.wav`. Luego, con `scipy.io.wavfile.write` se escribió el audio grabado en ese archivo.

## 6. ¿Qué diferencia hay entre `voz_archivo.py` y `voz_comandos.py`?

`voz_archivo.py` se centra en el reconocimiento de voz a partir de archivos de audio pregrabados, mientras que `voz_comandos.py` está diseñado para reconocer comandos de voz en tiempo real a través del micrófono.

## 7. Menciona un comando que implementaste y explica cómo funciona.

Un comando que implementé es "traducir". Este comando permite al usuario traducir un texto a otro idioma utilizando la API de Google Translate. Cuando el usuario dice "traducir" seguido del texto a traducir, el sistema captura el audio, lo convierte a texto y luego llama a la función `translate_text` para realizar la traducción.

# 8. ¿Qué posibles aplicaciones reales tiene un sistema de voz como este?

- Asistentes virtuales para el hogar.
- Sistemas de dictado para la transcripción de documentos.
- Herramientas de accesibilidad para personas con discapacidades.

## 9. ¿Cómo manejarías el error de conexión con el servicio de reconocimiento?

Para manejar el error de conexión con el servicio de reconocimiento, implementaría un bloque `try-except` alrededor de la llamada a la API. Si se produce un error de conexión, se podría mostrar un mensaje al usuario indicando que no se pudo conectar al servicio y ofrecer la opción de reintentar.

## 10. ¿Qué mejoras propondrías para la próxima versión de este asistente de voz?

- Mejorar la precisión del reconocimiento de voz entrenando modelos personalizados.
- Implementar soporte para múltiples idiomas y dialectos.
- Añadir la capacidad de realizar tareas más complejas mediante la comprensión del contexto.

## Preparación del entorno

Para el entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

Para instalar dependencias
```bash
pip install -r requirements.txt
```

## Ejecución

Para correr el programa usar el siguiente comando:
```bash
python voz_archivo.py
```
