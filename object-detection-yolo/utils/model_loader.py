from ultralytics import YOLO

def load_model(model_path="yolov8n.pt"):
    """Carga y devuelve un modelo YOLOv8."""
    return YOLO(model_path)
