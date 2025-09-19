# ai_folder/test_webcam.py

import cv2
from yolo_detector import ObjectDetector

def main():
    detector = ObjectDetector()
    cap = cv2.VideoCapture(0)  # 0 = default laptop camera

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera not found!")
            break
        output_img, detections = detector.detect_from_frame(frame)
        cv2.imshow("YOLOv8 Detection", output_img)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "_main_":
    main()