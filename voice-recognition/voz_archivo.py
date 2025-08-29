import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import tempfile, os
from voz_comandos import execute_command

# constantes
SRATE = 16000     # tasa de muestreo
DUR = 5           # segundos

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

