import mediapipe as mp
import cv2
import numpy as np
from math import sqrt
import win32api
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

video = cv2.VideoCapture(0)  # Access the camera

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)  # Flip the image horizontally
        
        imageHeight, imageWidth, _ = image.shape

        results = hands.process(image)  # Process the image for hand landmarks
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert back to BGR for OpenCV visualization

        # If hand landmarks are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                )

                # Get coordinates for index fingertip and thumb tip
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                # Convert normalized coordinates to pixel coordinates
                index_x, index_y = int(index_finger_tip.x * imageWidth), int(index_finger_tip.y * imageHeight)
                thumb_x, thumb_y = int(thumb_tip.x * imageWidth), int(thumb_tip.y * imageHeight)

                # Move the mouse cursor
                win32api.SetCursorPos((index_x * 4, index_y * 4))  # Adjust scaling factor as needed

                # Calculate the Euclidean distance between the index fingertip and thumb tip
                distance = sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2)

                # Detect a click based on the distance threshold
                if distance < 30:  # Adjust the threshold as necessary
                    pyautogui.click()
                    print("Mouse click detected")

        cv2.imshow('Hand Tracking', image)

        # Break the loop on pressing 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
