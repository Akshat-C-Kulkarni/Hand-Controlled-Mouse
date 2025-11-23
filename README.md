# ✋ Hand-Controlled Mouse Using Gestures
<hr>

## 🎯 Aim

To develop a computer vision–based system that enables users to control mouse movements and actions using hand gestures captured through a webcam—eliminating the need for a physical mouse.
<hr>

## 🧠 Description

This project uses MediaPipe Hands, OpenCV, and Python automation libraries to detect real-time hand landmarks and map specific gestures to mouse actions such as cursor movement, clicking, and scrolling.

Instead of training an ML model, this system uses rule-based gesture classification derived from finger positions and landmark geometry.
A pinky-based pointing mechanism combined with smoothing ensures stable and responsive cursor movement.

The final system operates entirely locally, requires no additional hardware, and provides an intuitive demonstration of human–computer interaction using computer vision.
<hr>

## 📹 Demonstration

The program displays a live webcam feed (kept always-on-top) showing:
- Real-time hand landmarks
- Cursor responses
- Gesture behavior for clicks and scrolling
This feed can be placed in any corner of the screen to record a clean demo video.
<hr>

## ⚙️ Project Structure

hand-controlled-mouse/<br>
│<br>
├── app/     # Core Python scripts (hand tracking, mouse control, gesture logic)<br>
├── data/     # Optional storage for future datasets or calibration (empty)<br>
├── model/     # (Not required for this project — rule-based system)<br>
├── README.md   # Project documentation<br>
└── requirements.txt   # Python dependencies<br>
<hr>

## ✋ Gestures Implemented

| Gesture        | Hand Pose                                  | Action                           |<br>
|----------------|--- ----------------------------------------|----------------------------------|<br>
| **Move**       | All fingers up                             | Cursor follows pinky fingertip   |<br>
| **Left Click** | Index finger down (others up)              | Performs a left-click            |<br>
| **Right Click**| Ring finger down (others up)               | Performs a right-click           |<br>
| **Scroll Up**  | Index + middle up, others down             | Scrolls upward                   |<br>
| **Scroll Down**| IM below wrist (while in scroll-up pose)   | Scrolls downward                 |<br>
| **None**       | All fingers down                           | Stops cursor movement            |<br>

<hr>

## 🧩 Core Components

1. Hand Tracking
- MediaPipe Hands used for detecting the wrist + 21 finger landmarks
- Real-time prediction at ~30 FPS
- Coordinate normalization and margin correction improve usable range

2. Gesture Classification (Rule-Based)
- Finger-up/down detection using relative landmark positions
- No ML model required
- Robust and lightweight gesture logic

3. Mouse Control
- Cursor control using pynput and pyautogui
- Pinky-based pointing added for higher stability
- Exponential smoothing to reduce jitter
- Click and scroll cooldowns to prevent accidental triggers

4. Always-on-Top Window
- Webcam preview stays visible even while interacting with the desktop
- Implemented using Win32 API
<hr>

## 🚀 Output

A fully functional gesture-based mouse system that enables:
- Hands-free cursor control
- Left and right clicks
- Smooth scrolling
- Real-time gesture visualization
- Webcam window pinned on top for demos
This can be showcased in videos or used as an assistive tool prototype.
<hr>

## 📦 How to Run the Application

1. Install dependencies
pip install -r requirements.txt

2. Run the program
python app/hand_tracking.py

3. Place your hand in front of webcam
Perform gestures to move the cursor, click, or scroll.
<hr>

## 📈 Outcomes

- Built a gesture-driven Human–Computer Interaction (HCI) prototype
- Combined computer vision, automation, and gesture logic in one project
- Gained hands-on experience with MediaPipe, OpenCV, and PyAutoGUI
- Fine-tuned smoothing, mapping, and gesture thresholds for stability
- Delivered a demo-ready, visually appealing system
<hr>

## 🔮 Future Improvements

- Add calibration mode for personalized movement range
- Implement gesture confidence scoring
- Add two-hand gestures (zoom in/out, drag-and-drop)
- Add visual overlays with gesture labels and confidence heatmaps
- Package the system as a desktop tool using PyInstaller
- Add voice-feedback for detected gestures