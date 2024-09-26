import cv2
import mediapipe as mp
import time
import requests

time.sleep(2.0)
current_key_pressed = set()

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]
server_ip = "192.168.4.1"  # Replace with the IP address of your Arduino server
# Define the coordinates of the square
square_x1, square_y1 = 210, 100  # Top-left corner coordinates
square_x2, square_y2 = square_x1 + 250, square_y1 + 180  # Bottom-right corner coordinates

video = cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.5,
                   min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if hand_landmarks.landmark[mp_hand.HandLandmark.WRIST].x < hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP].x:
                    # Detecting only the right hand
                    for id, lm in enumerate(hand_landmarks.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                    mp_draw.draw_landmarks(image, hand_landmarks, mp_hand.HAND_CONNECTIONS)
                    break  # Exit the loop after detecting the right hand
        
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
            elif total in range(1, 6):
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, f"{total}", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 0, 0), 5)
        else:
            total = 0  # If no hand is detected, set total to 0

        # Draw the square on the frame
        cv2.rectangle(image, (square_x1, square_y1), (square_x2, square_y2), (155, 0, 0), 2)
        cv2.putText(image, "Place your hand here", (square_x1, square_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Check if any hand landmark is within the square
        hand_in_square = any(square_x1 < lm[1] < square_x2 and square_y1 < lm[2] < square_y2 for lm in lmList)

        # If a hand is detected within the square, perform actions
        if hand_in_square:
           # time.sleep(1.0)
            requests.get(f"http://{server_ip}/data/?sensor_reading={{\"sensor0_reading\":{total}}}")
        else:
            total = 0  # If no hand is detected, set total to 0
            requests.get(f"http://{server_ip}/data/?sensor_reading={{\"sensor0_reading\":{total}}}")   
        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
video.release()
cv2.destroyAllWindows()
