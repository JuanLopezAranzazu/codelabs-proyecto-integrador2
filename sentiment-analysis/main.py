import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import make_pipeline
import joblib

# ----------------------------
# 1) Cargar dataset limpio
# ----------------------------
df = pd.read_csv("data/dataset_clean.csv")

print("Muestras:", df.shape[0],
      "| Positivos:", df["Sentiment"].sum(),
      "| Negativos:", len(df)-df["Sentiment"].sum())

# ----------------------------
# 2) Split estratificado
# ----------------------------
X_train_text, X_test_text, y_train, y_test = train_test_split(
    df["Text_clean"], df["Sentiment"],
    test_size=0.2, random_state=42, stratify=df["Sentiment"]
)

mayoritaria = int(round(y_train.mean()))
baseline = (y_test == mayoritaria).mean()
print(f"Baseline (clase mayoritaria): {baseline:.3f}")

# ----------------------------
# 3) Vectorizador + SVM
# ----------------------------
vectorizer = TfidfVectorizer(max_features=30000, ngram_range=(1,2), min_df=2)
X_train = vectorizer.fit_transform(X_train_text)
X_test  = vectorizer.transform(X_test_text)

clf = LinearSVC(class_weight="balanced", random_state=42)
clf.fit(X_train, y_train)

# ----------------------------
# 4) Evaluación
# ----------------------------
pred = clf.predict(X_test)
acc = accuracy_score(y_test, pred)
print(f"\nAccuracy en test: {acc:.3f}  |  Mejora vs baseline: {acc - baseline:.3f}\n")
print("Reporte por clase:")
print(classification_report(y_test, pred, digits=3))

cm = confusion_matrix(y_test, pred, labels=[0,1])
print("\nMatriz de confusión:")
print(pd.DataFrame(cm,
                   index=["Real 0 (neg)", "Real 1 (pos)"],
                   columns=["Pred 0 (neg)", "Pred 1 (pos)"]))

# ----------------------------
# 5) Validación cruzada
# ----------------------------
pipe = make_pipeline(
    TfidfVectorizer(max_features=30000, ngram_range=(1,2), min_df=2),
    LinearSVC(class_weight="balanced", random_state=42)
)
scores = cross_val_score(pipe, df["Text_clean"], df["Sentiment"],
                         cv=5, scoring="f1_macro")
print(f"\nCV (5-fold) F1_macro: media={scores.mean():.3f}  ±{scores.std():.3f}")

# ----------------------------
# 6) Guardar modelo
# ----------------------------
joblib.dump(vectorizer, "tfidf.joblib")
joblib.dump(clf, "modelo.joblib")
print("\nModelo y vectorizador guardados.")

# ----------------------------
# 7) Ejemplo de predicción en español
# ----------------------------
# Cargar vectorizador y modelo
vectorizer = joblib.load("tfidf.joblib")
clf = joblib.load("modelo.joblib")

# Nuevos ejemplos (en español)
ejemplos = [
    "Me encantó este producto, es fantástico.",     # positivo
    "El servicio fue pésimo y me trataron mal.",    # negativo
    "La película estuvo increíble, la volvería a ver.",  # positivo
    "El envío llegó dañado y muy tarde.",           # negativo
]

# Transformar y predecir
X_new = vectorizer.transform(ejemplos)
preds = clf.predict(X_new)

# Mostrar resultados
for texto, etiqueta in zip(ejemplos, preds):
    sentimiento = "Positivo 😊" if etiqueta == 1 else "Negativo 😡"
    print(f"Texto: {texto}\n → Predicción: {sentimiento}\n")
