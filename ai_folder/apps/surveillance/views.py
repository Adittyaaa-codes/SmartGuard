# apps/surveillance/views.py

from django.shortcuts import render
from django.http import JsonResponse
from ai_folder.yolo_detector import DefenseDetector
import cv2
import base64

# Initialize the detector once at startup
detector = DefenseDetector()

def dashboard(request):
    """
    Renders the main surveillance dashboard.
    """
    return render(request, 'surveillance/dashboard.html', {
        'total_cameras': 12,
        'active_drones': 3,
        'system_status': 'Online',
    })

def analyze_frame(request):
    """
    Captures a frame from the default webcam, runs threat detection,
    and returns the detections as JSON.
    """
    cap = cv2.VideoCapture(0)  # 0 for default laptop webcam
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return JsonResponse({'success': False, 'error': 'Unable to read from camera'}, status=500)

    # Run detection and get annotated frame + detections
    annotated_frame, detections = detector.detect_persons(frame)

    # Encode the annotated frame as JPEG to send back
    _, buffer = cv2.imencode('.jpg', annotated_frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')

    return JsonResponse({
        'success': True,
        'detections': detections,
        'frame': jpg_as_text,
    })