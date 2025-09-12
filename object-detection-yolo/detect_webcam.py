import cv2
from utils.model_loader import load_model

def detect_webcam():
    model = load_model()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        annotated = results[0].plot()

        cv2.imshow("Detección YOLOv8", annotated)

        # Para salir del programa
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

detect_webcam()
