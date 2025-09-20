import cv2, os, imagehash, hashlib
from PIL import Image
from tqdm import tqdm
from roboflow import Roboflow

# Roboflow setup (replace with your actual values)
rf = Roboflow(api_key="EJI3GWljQHGWxShDqKu6")          
project = rf.workspace("your-workspace").project("sharp-objects")

# Image collection logic
SAVE_DIR = "captures"; os.makedirs(SAVE_DIR, exist_ok=True)
seen = set()                                   
cap  = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

print("Image collection started!")
print("SPACE saves image / Q quits")

pbar = tqdm(total=200)                         
while pbar.n < 200:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from camera")
        break
        
    # Display camera feed
    cv2.imshow("SPACE saves / Q quits", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == 32:              # SPACE key
        img_name = f"{pbar.n:04}.jpg"; path = f"{SAVE_DIR}/{img_name}"
        cv2.imwrite(path, frame)
        h = imagehash.phash(Image.open(path))  
        if h in seen: 
            os.remove(path)
            print(f"Duplicate image detected, skipping...")
            continue
        seen.add(h); pbar.update(1)
        print(f"Captured: {img_name}")
    elif key == ord('q'):      # Q key
        break

cap.release()
cv2.destroyAllWindows()
print(f"\nCollection complete! Captured {pbar.n} unique images in '{SAVE_DIR}' folder")
