# Codelab Entrenamiento Yolo con el universo de Roboflow

## Crear cuenta y copiar tu API key

1. Ve a https://roboflow.com y crea cuenta (Google o correo).
2. Haz clic en tu avatar (arriba a la derecha) Settings / Account.
3. En API Keys (o Roboflow API), copia tu API key.

Agregar al archivo .env
```bash
ROBOFLOW_API_KEY="your_roboflow_api_key"
```

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

## Descargar el dataset

```bash
python dataset.py
```

## Entrenar YOLOv8 con el dataset

Con el dataset descargado y `data.yaml` listo:
```bash
yolo detect train data=mask-wearing-1/data.yaml model=yolov8n.pt epochs=50 imgsz=640
```

## Ejecución

Para correr el programa usar el siguiente comando:
```bash
python detect_image.py
python detect_webcam.py
```
