# app/webcam_capture.py

import cv2
import time

def run_webcam():
    # Open webcam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW fixes delay on Windows

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Optional: Set resolution (improves FPS)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    p_time = 0  # previous timestamp

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame")
            break

        # Flip horizontally for a mirror-like view
        frame = cv2.flip(frame, 1)

        # FPS calculation
        c_time = time.time()
        fps = 1 / (c_time - p_time) if p_time != 0 else 0
        p_time = c_time

        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Webcam - Day 1", frame)

        # ESC or q to quit
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_webcam()
