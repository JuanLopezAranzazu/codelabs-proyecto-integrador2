from ultralytics import YOLO

model_yolo = YOLO("yolov8n.pt")
results = model_yolo("perros.jpg")
results[0].show()
