import cv2
import time

print("--- STARTING CAMERA CHECK ---")
print("1. Opening Camera (Index 0)...")

# Try index 0. If you still get errors later, change this to 1
cap = cv2.VideoCapture(0)

# Set resolution to 640x480 (Standard for Pi)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("FAIL: Could not open camera. (Did you use libcamerify?)")
    exit()

print("2. Camera Opened! Warming up sensors...")

# --- THE WARM UP LOOP ---
# We read 30 frames just to throw them away. 
# This gives the camera time to adjust to the light in your room.
for i in range(30):
    ret, frame = cap.read()
    if i % 10 == 0:
        print(f"   ... reading frame {i}/30")
    time.sleep(0.05)

print("3. Taking the final picture...")
# Now we take the REAL picture
ret, frame = cap.read()

if ret:
    print(f"SUCCESS! Captured an image. Size: {frame.shape}")
    # Save it to your folder so you can see it
    filename = "proof_it_works.jpg"
    cv2.imwrite(filename, frame)
    print(f"Saved image as '{filename}'. Go check your folder!")
else:
    print("FAIL: The camera returned an empty frame (None).")

cap.release()
print("--- TEST COMPLETE ---") 