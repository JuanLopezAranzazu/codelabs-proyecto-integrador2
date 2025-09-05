import cv2
import numpy as np
import matplotlib.pyplot as plt
from mtcnn.mtcnn import MTCNN
from time import time

# Carga imagen (sube archivos en Colab o usa una URL y descárgala)
img = cv2.imread('grupo.jpg')  # reemplaza por tu archivo
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

detector = MTCNN()   # puedes ajustar min_face_size
t0 = time()
res = detector.detect_faces(img_rgb)
t1 = time()

print(f"Detected: {len(res)} rostro(s) • tiempo: {(t1 - t0)*1000:.1f} ms")
for r in res:
    print(r['confidence'], r['box'], r['keypoints'].keys())


vis = img_rgb.copy()
for r in res:
    x, y, w, h = r['box']
    cv2.rectangle(vis, (x,y), (x+w, y+h), (0,255,0), 2)
    for name, (px,py) in r['keypoints'].items():
        cv2.circle(vis, (px,py), 2, (255,0,0), -1)
plt.imshow(vis)
plt.axis('off')
plt.show()


detector = MTCNN()  # su NMS interno filtra solapes
# Prueba filtrado por confianza mínima
thr = 0.90
filtrados = [r for r in res if r['confidence'] >= thr]
print(f"Con thr={thr} quedan {len(filtrados)} rostros")
