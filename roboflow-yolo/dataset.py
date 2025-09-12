import os
from roboflow import Roboflow

# Variables del dataset
WORKSPACE="roboflow-100"
DATASET_NAME="mask-wearing-608pr"

rf = Roboflow(api_key=os.environ["ROBOFLOW_API_KEY"])
project = rf.workspace(WORKSPACE).project(DATASET_NAME)  # cambia si usas otro dataset
dataset = project.version(1).download("yolov8")  # revisa la versión disponible
