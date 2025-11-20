# app/hand_tracking.py

import cv2
import mediapipe as mp
import time
from gesture_detector import detect_gesture
from pynput.mouse import Button, Controller
from mouse_controller import move_cursor, left_click, right_click, scroll_vertical
import pyautogui  # for screen size
prev_scroll_y = None

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def run_hand_tracking():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not access webcam.")
        return

    # Lower resolution for smoother performance if needed
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    p_time = 0

    # Initialize MediaPipe Hands
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:

        while True:
            success, frame = cap.read()
            if not success:
                print("Failed to grab frame")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process frame
            results = hands.process(rgb)

            # Draw landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                    )
            
            # ------------ Gesture Testing -------------
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]  # primary hand
                gesture_result = detect_gesture(hand_landmarks.landmark, None)
                g = gesture_result["gesture"]
                data = gesture_result.get("data", {})
                gesture = gesture_result["gesture"]
                if gesture == "move":
                    lm = hand_landmarks.landmark[8]
                    screen_w, screen_h = pyautogui.size()
                    move_cursor(lm.x, lm.y, screen_w, screen_h)

                elif gesture == "left_click":
                    left_click()

                elif gesture == "right_click":
                    right_click()

                elif gesture == "scroll":
                    lm = hand_landmarks.landmark[8]   # index fingertip
                    y = lm.y

                    global prev_scroll_y
                    if prev_scroll_y is None:
                        prev_scroll_y = y

                    dy = prev_scroll_y - y   # positive: hand moved up → scroll up

                    # Sensitivity multiplier
                    SCROLL_SENS = 80

                    delta = int(dy * SCROLL_SENS)

                    if delta != 0:
                        scroll_vertical(delta)

                    prev_scroll_y = y



            # FPS counter
            c_time = time.time()
            fps = 1 / (c_time - p_time) if p_time > 0 else 0
            p_time = c_time

            # Display info
            cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            if results.multi_hand_landmarks:
                count = len(results.multi_hand_landmarks)
            else:
                count = 0

            cv2.putText(frame, f'Hands: {count}', (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("Hand Gesture Testing - Day 2", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_hand_tracking()
