import json
import cv2
from utils.model_loader import load_model

def export_results(image_path="perros.jpg", output_json="resultados.json"):
    model = load_model()
    frame = cv2.imread(image_path)
    results = model(frame)

    detecciones = []
    for r in results[0].boxes:
        obj = {
            "clase": model.names[int(r.cls)],
            "score": float(r.conf),
            "bbox": r.xyxy.tolist()[0]
        }
        detecciones.append(obj)

    with open(output_json, "w") as f:
        json.dump(detecciones, f, indent=4)

    print(f"Resultados exportados a {output_json}")

export_results()
