import cv2

print("Testing OpenCV GUI functionality...")

# Test basic window creation
test_image = cv2.imread('yolov8n.pt', 0)  # Try to read any file as grayscale
if test_image is None:
    # Create a simple test image if no file available
    import numpy as np
    test_image = np.zeros((300, 400), dtype=np.uint8)
    cv2.putText(test_image, "GUI TEST", (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255), 2)

try:
    cv2.imshow('OpenCV GUI Test', test_image)
    print("✅ GUI window created successfully!")
    print("Press any key in the window to close...")
    cv2.waitKey(5000)  # Wait 5 seconds or until key press
    cv2.destroyAllWindows()
    print("✅ OpenCV GUI is working properly!")
except Exception as e:
    print(f"❌ GUI Error: {e}")