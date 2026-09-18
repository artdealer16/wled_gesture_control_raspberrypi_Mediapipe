import cv2

# We assume index 0. If Step 2 showed valid numbers like video2, 
# you might change this to 2.
cap = cv2.VideoCapture(0)

if cap.isOpened():
    print("SUCCESS: Python can talk to the Webcam!")
    # Let's be nosy and ask how big the picture is
    width = cap.get(3)  # 3 is the code for Width
    height = cap.get(4) # 4 is the code for Height
    print(f"Resolution: {width} x {height}")
else:
    print("FAILURE: Python cannot open the camera.")

cap.release()