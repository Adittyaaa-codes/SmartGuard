# ai_models/yolo_detector.py
from ultralytics import YOLO
import cv2
import numpy as np
from .models import MODEL_PATH

MODEL_PATH = "ai_models/models/yolov8n.pt"

class ObjectDetector:
    def _init_(self, model_path=MODEL_PATH):
        self.model = YOLO(model_path)

    def detect_from_frame(self, frame):
        results = self.model(frame)[0]
        output = frame.copy()
        detections = []
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]
            cv2.rectangle(output, (x1, y1), (x2, y2), (0,255,0), 2)
            label = f'{class_name} {confidence:.2f}'
            cv2.putText(output, label, (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            detections.append({'bbox':[x1,y1,x2,y2],
                               'confidence':confidence,
                               'class':class_name})
            
        return output, detections