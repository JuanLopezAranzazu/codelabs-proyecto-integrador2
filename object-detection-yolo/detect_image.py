import time
from utils.model_loader import load_model

def detect_on_image(image_path="perros.jpg", output_path="resultado_yolo.jpg"):
    model = load_model()
    t2 = time.time()
    results = model(image_path)
    t3 = time.time()

    print(f"Tiempo de inferencia: {t3 - t2:.2f} s")

    for r in results:
        print(r.names)
        print(r.boxes)

    results[0].save(filename=output_path)
    print(f"Imagen guardada en {output_path}")

detect_on_image()
