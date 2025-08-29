import webbrowser
from datetime import datetime
import pyjokes
import asyncio
from googletrans import Translator

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

    elif "buscar" in command:
        term = command.split("buscar")[1].strip()
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
