import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import make_pipeline
import joblib

from utils import clean_text

# ----------------------------
# 1) Dataset sintético realista
# ----------------------------
random.seed(42)
np.random.seed(42)

positive_reviews = [
    "Excelente servicio", "Muy buena atención", "Me encantó el producto",
    "Rápido y confiable", "Todo llegó perfecto", "Calidad superior",
    "Lo recomiendo totalmente", "Volveré a comprar", "Precio justo y buena calidad",
    "El soporte fue amable", "Experiencia increíble", "Funcionó mejor de lo esperado",
    "Entregado a tiempo", "Muy satisfecho", "Cinco estrellas",
    "La comida estaba deliciosa", "El empaque impecable", "Súper recomendable",
    "Buen trato del personal", "Gran experiencia"
]

negative_reviews = [
    "Pésimo servicio", "Muy mala atención", "Odio este producto",
    "Lento y poco confiable", "Llegó dañado", "Calidad terrible",
    "No lo recomiendo", "No vuelvo a comprar", "Caro y mala calidad",
    "El soporte fue grosero", "Experiencia horrible", "Peor de lo esperado",
    "Entregado tarde", "Muy decepcionado", "Una estrella",
    "La comida estaba fría", "El empaque roto", "Nada recomendable",
    "Mal trato del personal", "Mala experiencia"
]

# Función para agregar variantes de los textos (emojis, énfasis)
def add_variants(phrase):
    extras = ["", "!", "!!", " 🙂", " 😡", " de verdad", " en serio", " 10/10", " 1/10",
              " súper", " la verdad", " jamás", " nunca", " para nada"]
    return phrase + random.choice(extras)

# Aumentar dataset
pos = [add_variants(p) for _ in range(8) for p in positive_reviews]
neg = [add_variants(n) for _ in range(8) for n in negative_reviews]

texts = pos + neg
labels = [1]*len(pos) + [0]*len(neg)  # 1=positivo, 0=negativo

df = pd.DataFrame({"text": texts, "label": labels}).sample(frac=1, random_state=42).reset_index(drop=True)
print("Muestras:", df.shape[0], "| Positivos:", df.label.sum(), "| Negativos:", len(df)-df.label.sum())

# ----------------------------
# 2) Limpieza simple de los textos
# ----------------------------
df["text_clean"] = df["text"].apply(clean_text)

# ----------------------------
# 3) División estratificada + baseline
# ----------------------------
X_train_text, X_test_text, y_train, y_test = train_test_split(
    df["text_clean"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

majority_class = int(round(y_train.mean()))
baseline = (y_test == majority_class).mean()
print(f"Baseline (clase mayoritaria): {baseline:.3f}")

# ----------------------------
# 4) Vectorizador TF-IDF + SVM lineal
# ----------------------------
vectorizer = TfidfVectorizer(max_features=30000, ngram_range=(1,2), min_df=2)

X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)

clf = LinearSVC(class_weight="balanced", random_state=42)
clf.fit(X_train, y_train)

# ----------------------------
# 5) Evaluación del modelo
# ----------------------------
pred = clf.predict(X_test)
acc = accuracy_score(y_test, pred)
print(f"\nAccuracy en test: {acc:.3f} | Mejora vs baseline: {acc - baseline:.3f}\n")
print("Reporte de clasificación:")
print(classification_report(y_test, pred, digits=3))

cm = confusion_matrix(y_test, pred, labels=[0,1])
print("\nMatriz de confusión:")
print(pd.DataFrame(cm, index=["Real 0 (neg)", "Real 1 (pos)"], columns=["Pred 0 (neg)", "Pred 1 (pos)"]))

# ----------------------------
# 6) Validación cruzada
# ----------------------------
pipe = make_pipeline(
    TfidfVectorizer(max_features=30000, ngram_range=(1,2), min_df=2),
    LinearSVC(class_weight="balanced", random_state=42)
)
scores = cross_val_score(pipe, df["text_clean"], df["label"], cv=5, scoring="f1_macro")
print(f"\nValidación cruzada (5-fold) F1_macro: media={scores.mean():.3f} ± {scores.std():.3f}")

# ----------------------------
# 7) Guardar modelo y vectorizador
# ----------------------------
joblib.dump(vectorizer, "tfidf_vectorizer.joblib")
joblib.dump(clf, "sentiment_model.joblib")
print("\nModelo y vectorizador guardados.")
