import speech_recognition as sr
from voice_commands import execute_command

# constantes
WAKE_WORD = "alexa"


# obtener audio
def get_audio():
    r = sr.Recognizer()
    status = False
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        rec = ""

        try:
            rec = r.recognize_google(audio, language='es-ES').lower()

            if WAKE_WORD in rec:
                rec = rec.replace(f"{WAKE_WORD} ", "")
                rec = rec.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                status = True

        except sr.UnknownValueError:
            print("No se entendió el audio.")

        except sr.RequestError as e:
            print("Error:", e)

    return rec, status


# loop
def main():
    while True:
        print("Escuchando...")
        rec, status = get_audio()

        if status:
            print("Dijiste:", rec)
            execute_command(rec)


# iniciar
if __name__ == "__main__":
    main()
