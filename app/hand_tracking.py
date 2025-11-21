# app/hand_tracking.py

import cv2
import mediapipe as mp
import time
import win32gui
import win32con
from gesture_detector import detect_gesture
from mouse_controller import (
    move_cursor,
    left_click,
    right_click,
    scroll_vertical,
    reset_smoothing_state,
)
import pyautogui

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

prev_gesture = "none"

CLICK_COOLDOWN = 0.5
last_left_click = 0
last_right_click = 0

MOVE_DELAY = 0.005
last_move = 0

# SCROLL
SCROLL_COOLDOWN = 0.03
last_scroll = 0
_prev_scroll = 0.0
SMOOTH_SCROLL_ALPHA = 0.20
SCROLL_SPEED = 20   # VERY SLOW SCROLL


def run_hand_tracking():

    global prev_gesture, last_left_click, last_right_click
    global last_move, last_scroll, _prev_scroll

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # ---------------------------
    # Create the window first so we can set always-on-top
    # ---------------------------
    cv2.namedWindow("Gesture Mouse", cv2.WINDOW_NORMAL)

    # Force window always on top (Windows only)
    try:
        hwnd = win32gui.FindWindow(None, "Gesture Mouse")
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
        )
    except:
        print("Warning: Could not force window to topmost.")

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:

        while True:

            ok, frame = cap.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            if results.multi_hand_landmarks:

                h, w, _ = frame.shape
                hand = results.multi_hand_landmarks[0]

                mp_drawing.draw_landmarks(
                    frame, hand, mp_hands.HAND_CONNECTIONS
                )

                # Detect gesture
                gesture = detect_gesture(hand.landmark)["gesture"]

                # --------------------
                # MOVE (Original stable pinky-based version)
                # --------------------
                if gesture == "move":

                    if prev_gesture != "move":
                        reset_smoothing_state()

                    if time.time() - last_move > MOVE_DELAY:
                        last_move = time.time()

                        pinky = hand.landmark[20]

                        # Pixel coordinates
                        h, w, _ = frame.shape
                        pinky_x = int(pinky.x * w)
                        pinky_y = int(pinky.y * h)

                        # Small stable margin
                        margin_x = int(w * 0.01)
                        margin_y = int(h * 0.01)

                        pinky_x = max(margin_x, min(w - margin_x, pinky_x))
                        pinky_y = max(margin_y, min(h - margin_y, pinky_y))

                        # Normalize inside margins
                        norm_x = (pinky_x - margin_x) / (w - 2 * margin_x)
                        norm_y = (pinky_y - margin_y) / (h - 2 * margin_y)

                        # Slight overshoot scaling for better corner reach
                        norm_x = pow(norm_x, 0.95)
                        norm_y = pow(norm_y, 0.95)

                        norm_x = max(0.0, min(1.0, norm_x))
                        norm_y = max(0.0, min(1.0, norm_y))

                        # Move pointer
                        screen_w, screen_h = pyautogui.size()
                        move_cursor(norm_x, norm_y, screen_w, screen_h)

                # --------------------
                # LEFT CLICK
                # --------------------
                elif gesture == "left_click":
                    if time.time() - last_left_click > CLICK_COOLDOWN:
                        last_left_click = time.time()
                        left_click()

                # --------------------
                # RIGHT CLICK
                # --------------------
                elif gesture == "right_click":
                    if time.time() - last_right_click > CLICK_COOLDOWN:
                        last_right_click = time.time()
                        right_click()

                # --------------------
                # SCROLL UP (gesture-based)
                # --------------------
                elif gesture == "scroll_up":
                    scroll_vertical(1)

                # --------------------
                # SCROLL DOWN (Y-level based)
                # --------------------
                else:
                    idx = hand.landmark[8].y
                    mid = hand.landmark[12].y
                    wrist = hand.landmark[0].y
                    ring = hand.landmark[16].y
                    pinky = hand.landmark[20].y

                    avg_im = (idx + mid) / 2
                    avg_ref = (wrist + ring + pinky) / 3

                    if avg_im > avg_ref + 0.02:
                        if time.time() - last_scroll > SCROLL_COOLDOWN:
                            last_scroll = time.time()
                            scroll_vertical(-1)

                prev_gesture = gesture

            cv2.imshow("Gesture Mouse", frame)

            if cv2.waitKey(1) & 0xFF in (27, ord('q')):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_hand_tracking()
