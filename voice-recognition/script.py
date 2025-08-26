import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import tempfile, os
import webbrowser
from datetime import datetime
import pyjokes
import asyncio
from googletrans import Translator

# constantes
SRATE = 16000     # tasa de muestreo
DUR = 5           # segundos

# traducir texto
async def translate_text(text):
    translator = Translator()
    translation = await translator.translate(text, dest="en")
    print(f"Traducción: {translation.text}")

# ejecutar comandos de voz
def execute_command(command):
    command = command.lower()

    if "hola" in command:
        print("¡Hola, bienvenido al curso!")

    elif "abrir google" in command:
        webbrowser.open("https://www.google.com")

    elif "buscar" in command and "en youtube" in command:
        term = command.split("buscar")[1].split("en youtube")[0].strip()
        url = f"https://www.youtube.com/results?search_query={term.replace(' ', '+')}"
        webbrowser.open(url)
    
    elif "clima actual en" in command:
        term = command.split("clima actual en")[1].strip()
        webbrowser.open(f"https://wttr.in/{term}?format=3")

    elif "cuéntame un chiste" in command:
        print(pyjokes.get_joke("es", "chuck"))

    elif "traducir" in command:
        text = command.split("traducir")[1].strip()
        asyncio.run(translate_text(text))

    elif "fecha" in command:
        print("Fecha actual:", datetime.now().strftime("%d/%m/%Y"))

    elif "hora" in command:
        print("Hora actual:", datetime.now().strftime("%H:%M"))

    else:
        print("Comando no reconocido.")


# grabar audio
print("Grabando... habla ahora!")
audio = sd.rec(int(DUR*SRATE), samplerate=SRATE, channels=1, dtype='int16')
sd.wait()
print("Listo, procesando...")

# guarda a WAV temporal
tmp_wav = tempfile.mktemp(suffix=".wav")
write(tmp_wav, SRATE, audio)

# reconoce con SpeechRecognition
r = sr.Recognizer()
with sr.AudioFile(tmp_wav) as source:
    data = r.record(source)

try:
    text = r.recognize_google(data, language="es-ES")
    print("Dijiste:", text)
    execute_command(text)

except sr.UnknownValueError:
    print("No se entendió el audio.")

except sr.RequestError as e:
    print("Error:", e)

finally:
    if os.path.exists(tmp_wav):
        os.remove(tmp_wav)

