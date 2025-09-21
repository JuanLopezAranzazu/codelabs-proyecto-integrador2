# FastAPI + NLP Clasificación de comentarios

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

## Entrenar el modelo

Para entrenar y guardar el modelo
```bash
python src/ml/train_model.py
```

## Ejecución

Para correr el programa usar el siguiente comando:
```bash
uvicorn src.main:app --reload # Puerto 8000 por defecto
uvicorn src.main:app --reload --port 8080 # Ejecutar en un puerto especifico
```