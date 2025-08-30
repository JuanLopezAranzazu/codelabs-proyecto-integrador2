import wikipedia
import webbrowser
from datetime import datetime

# ejecutar comandos de voz
def execute_command(command):

    if "hola" in command:
        print("¡Hola, ¿en qué puedo ayudarte?")

    # buscar en Google
    elif "buscar en google" in command:
        query = command.replace("buscar en google ", "").strip()

        if not query:
            print("No se proporcionó ningún término de búsqueda.")
            return
        
        webbrowser.open(f"https://www.google.com/search?q={query}")

    # buscar en Youtube
    elif "buscar en youtube" in command:
        query = command.replace("buscar en youtube ", "").strip()

        if not query:
            print("No se proporcionó ningún término de búsqueda.")
            return

        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    # buscar en Wikipedia
    elif "buscar" in command:
        query = command.replace("buscar ", "").strip()
        wikipedia.set_lang("es")

        if not query:
            print("No se proporcionó ningún término de búsqueda.")
            return

        try:
            summary = wikipedia.summary(query, sentences=1)
            print("Resultado de la búsqueda:", summary)

        except wikipedia.exceptions.DisambiguationError:
            print("Demasiadas opciones, intenta ser más específico.")

        except wikipedia.exceptions.PageError:
            print("No se encontró ningún artículo con ese nombre.")

    # obtener fecha
    elif "fecha" in command:
        print("Fecha actual:", datetime.now().strftime("%d/%m/%Y"))

    # obtener hora
    elif "hora" in command:
        print("Hora actual:", datetime.now().strftime("%H:%M"))

    # salir del programa
    elif "adios" in command:
        print("¡Hasta luego!")
        exit()

    else:
        print("Comando no reconocido.")
