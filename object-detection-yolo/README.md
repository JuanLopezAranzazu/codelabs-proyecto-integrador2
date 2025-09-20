# Codelab Detección de objetos en imágenes con Yolo Lite

## 1. ¿Cómo cambia la velocidad de detección entre imágenes y webcam?

En imágenes la detección suele ser más rápida porque es un solo procesamiento; con webcam debe hacerlo en tiempo real para cada frame, lo que demanda más recursos y puede reducir la velocidad.

## 2. ¿Qué limitaciones tiene YOLO-lite en objetos pequeños?

Tiene menor precisión para detectar objetos pequeños o muy cercanos entre sí, porque simplifica la red para ser más liviana y pierde detalle en las características finas.

## 3. ¿Dónde aplicarías esta técnica en un proyecto IoT o web?

- **IoT**: Cámaras inteligentes para seguridad, conteo de personas, detección de vehículos o monitoreo en fábricas.
- **Web**: Aplicaciones de análisis de imágenes subidas por usuarios (por ejemplo, etiquetar fotos, validar productos en e-commerce).

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

## Ejecución

Para correr el programa usar el siguiente comando:
```bash
python detect_image.py
python detect_webcam.py
python export_json.py
```
