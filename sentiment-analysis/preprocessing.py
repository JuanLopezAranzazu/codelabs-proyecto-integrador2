import re
from deep_translator import GoogleTranslator
import pandas as pd

# ----------------------------
# 1) Cargar y separar columnas
# ----------------------------
df_raw = pd.read_csv("data/dataset.csv", header=None)

# Separar por coma
df_split = df_raw[0].str.split(",", expand=True)

# Asignar nombres correctos
df_split.columns = ["Text", "Sentiment", "Source", "Date/Time", "User ID", "Location", "Confidence Score"]

# ----------------------------
# 2) Quedarse con texto y etiqueta
# ----------------------------
df = df_split[["Text", "Sentiment"]].copy()

# limpiar comillas
df["Text"] = df["Text"].str.replace('"', '', regex=False).str.strip()

# mapear etiquetas
df["Sentiment"] = df["Sentiment"].str.strip().map({"Positive": 1, "Negative": 0})

# quitar nulos
df = df.dropna(subset=["Text", "Sentiment"])

# ----------------------------
# 3) Traducir al español
# ----------------------------
translator = GoogleTranslator(source="en", target="es")
df["Text_es"] = df["Text"].apply(lambda x: translator.translate(x))

# ----------------------------
# 4) Limpieza de texto
# ----------------------------
def limpiar(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-záéíóúñü0-9\s]", " ", s)  # solo letras/números/espacios
    s = re.sub(r"\s+", " ", s).strip()
    return s

df["Text_clean"] = df["Text_es"].astype(str).apply(limpiar)

print(df.head())

# ----------------------------
# 5) Guardar dataset limpio
# ----------------------------
df.to_csv("data/dataset_clean.csv", index=False)
print("Dataset limpio guardado en data/dataset_clean.csv")
