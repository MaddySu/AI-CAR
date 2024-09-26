import cv2
import mediapipe as mp
import time
import requests
import tkinter as tk
from tkinter import messagebox

def send_sensor_reading(total):
    server_ip = "192.168.4.1"  # Replace with the IP address of your Arduino server
    try:
        response = requests.get(f"http://{server_ip}/data/?sensor_reading={{\"sensor0_reading\":{total}}}")
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        messagebox.showerror("Connection Error", "Please connect to Wi-Fi and try again.")
        print(e)

def start_camera_feed():
    time.sleep(2.0)
    current_key_pressed = set()

    mp_draw = mp.solutions.drawing_utils
    mp_hand = mp.solutions.hands

    tipIds = [4, 8, 12, 16, 20]

    video = cv2.VideoCapture(0)

    with mp_hand.Hands(min_detection_confidence=0.5,
                       min_tracking_confidence=0.5) as hands:
        hand_detected = False
        while True:
            ret, image = video.read()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            lmList = []

            # If no hand was previously detected, check for new hands
            if not hand_detected:
                if results.multi_hand_landmarks:
                    # Set hand_detected flag to True
                    hand_detected = True
                    myHands = results.multi_hand_landmarks[0]
                    for id, lm in enumerate(myHands.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                    mp_draw.draw_landmarks(image, myHands, mp_hand.HAND_CONNECTIONS)

            # If hand was previously detected, continue tracking until it's gone
            elif hand_detected:
                if results.multi_hand_landmarks:
                    myHands = results.multi_hand_landmarks[0]
                    for id, lm in enumerate(myHands.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                    mp_draw.draw_landmarks(image, myHands, mp_hand.HAND_CONNECTIONS)
                else:
                    # Reset hand_detected flag to False if no hand is detected
                    hand_detected = False

            fingers = []
            if len(lmList) != 0:
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                total = fingers.count(1)
                if total == 0:
                    cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, "0", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                                2, (255, 0, 0), 5)
                    send_sensor_reading(total)
                elif total in range(1, 6):
                    cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, f"{total}", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                                2, (255, 0, 0), 5)
                    send_sensor_reading(total)
            else:
                total = 0  # If no hand is detected, set total to 0
                send_sensor_reading(total)

            cv2.imshow("Frame", image)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break
    video.release()
    cv2.destroyAllWindows()

def on_start_button_click():
    start_camera_feed()

# Create the Tkinter window
root = tk.Tk()
root.title("Hand Detection Camera Feed")

# Create the start button
start_button = tk.Button(root, text="Start Camera Feed", command=on_start_button_click)
start_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
