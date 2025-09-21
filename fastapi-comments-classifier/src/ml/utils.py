import re

def clean_text(s: str) -> str:
    """
    Limpieza básica de texto: minúsculas, quitar caracteres no alfanuméricos, normalizar espacios.
    """
    s = s.lower()
    s = re.sub(r"[^a-záéíóúñü0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def predict_sentiment(model, vectorizer, text: str) -> str:
    """
    Predice si el texto es positivo o negativo usando el modelo entrenado.
    """
    text_clean = clean_text(text)
    X = vectorizer.transform([text_clean])
    return "positivo" if model.predict(X)[0] == 1 else "negativo"
