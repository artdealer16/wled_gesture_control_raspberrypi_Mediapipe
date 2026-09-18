import cv2
import mediapipe as mp
import requests
import time

# --- SETUP ---
WLED_IP = '172.20.10.3'
WLED_API = 'http://172.20.10.3/json/state'

# --- THE HELPER FUNCTION ---
def lighting(gesture_code):
    # -1: TURN OFF
    if gesture_code == -1:
        data = {"on": False}
        print('   >>> Sending: Light OFF')

    # 100: FIST -> SOLID RED (Vibrant Warning)
    elif gesture_code == 100:
        data = {
            "on": True,
            "bri": 255, # Force Max Brightness
            "seg": [{
                "col": [[255, 0, 0]], # Pure Red
                "fx": 0,              # Solid (No movement)
                "sx": 0                # Speed 0
            }]
        }
        print('   >>> Sending: Solid Red')

    # 15: ONE FINGER -> PARTY MODE (Multi-Color)
    elif gesture_code == 54:
        data = {
            "on": True,
            "bri": 255,
            "seg": [{
                "pal": 38,    # "Party" Palette (Vibrant mix)
                "fx": 75,    # "Breath" Effect (Pulses the colors)
                "sx": 228,   # Medium Speed
                "ix": 128    # Medium Intensity
            }]
        }
        print('   >>> Sending: Party Mode')

    # 3: PEACE SIGN -> RAINBOW (Neon Vibe)
    elif gesture_code == 48:
        data = {
            "on": True,
            "bri": 255,
            "seg": [{
                "pal": 20,   # "Rainbow" Palette
                "fx": 117,   # "Percent" Effect (Moves colors across strip)
                "sx": 64,    # Slower, chill speed
                "ix": 128
            }]
        }
        print('   >>> Sending: Rainbow Flow')

    # 10: OPEN HAND -> OCEAN (Bright Blue/Teal)
    else:
        # Default for Open Hand (Code 10)
        data = {
            "on": True,
            "bri": 255,
            "seg": [{
                "pal": 3,    # "Ocean" Palette
                "fx": 33,    # "Flow" Effect (Smooth water movement)
                "sx": 128,
                "ix": 128
            }]
        }
        print(f'   >>> Sending: Ocean Mode (Code {gesture_code})')

    try:
        requests.post(WLED_API, json=data)
    except:
        print(f'Error connecting to WLED:{e}')

# --- INITIALIZATION ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=.7)
mp_draw = mp.solutions.drawing_utils

# We are sticking with 'cam_cap' since that is what you chose!

cam_cap = cv2.VideoCapture(0)

print("SYSTEM READY: The setup finished successfully!")
print("Starting the Loop... Press 'q' to quit.")

last_gesture = None

# --- MAIN LOOP ---
while True:
    
    success, img = cam_cap.read()
    if not success:
        break 

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # --- DEFAULT STATE (AUTO-OFF LOGIC) ---
    # We set this to -1 (OFF) every single frame.
    # If a hand is found below, we will overwrite this with the real gesture.
    # If NO hand is found, this stays -1, and the lights turn off.
    current_gesture = -1

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Define Points
            index_tip = hand_landmarks.landmark[8].y
            knuckle = hand_landmarks.landmark[5].y
            
            middle_tip = hand_landmarks.landmark[12].y
            third_knuckle = hand_landmarks.landmark[9].y
            
            ring_tip = hand_landmarks.landmark[16].y
            fourth_knuckle = hand_landmarks.landmark[13].y
            
            pinky_tip = hand_landmarks.landmark[20].y
            fifth_knuckle = hand_landmarks.landmark[17].y
            
            # Count Fingers
            fingers_up = 0
            
            if index_tip < knuckle:
                fingers_up += 1
            if middle_tip < third_knuckle:
                fingers_up += 1
            if ring_tip < fourth_knuckle:
                fingers_up += 1
            if pinky_tip < fifth_knuckle:
                fingers_up += 1
            
            # Decide Gesture
            if fingers_up == 0:
                current_gesture = 100 # FIST -> GREEN
                print('Fist detected')
            
            elif fingers_up == 1:
                current_gesture = 54  # ONE FINGER -> PALETTE 15
                print('One finger up')
            
            elif fingers_up == 2:
                current_gesture = 3   # PEACE -> PALETTE 3
                print('Peace sign detected')
            
            elif fingers_up >= 4:
                current_gesture = 48  # OPEN -> PALETTE 10
                print('Open hand detected')

    # --- THE GATEKEEPER ---
    # 1. If current_gesture is different from the last one sent...
    # 2. AND it is not None (just in case)...
    # Then send the command.
    if current_gesture != last_gesture:
        lighting(current_gesture)
        last_gesture = current_gesture
                  
    cv2.imshow("Gesture Lamp", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cam_cap.release()
cv2.destroyAllWindows()