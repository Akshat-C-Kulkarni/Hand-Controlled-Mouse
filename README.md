<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 200" width="900" height="200">
  <defs>
    <linearGradient id="bg3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#042f2e"/>
      <stop offset="100%" style="stop-color:#0f172a"/>
    </linearGradient>
    <linearGradient id="acc3" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#34d399"/>
      <stop offset="100%" style="stop-color:#06b6d4"/>
    </linearGradient>
  </defs>
  <rect width="900" height="200" fill="url(#bg3)" rx="12"/>
  <!-- Hand landmark dots -->
  <circle cx="760" cy="100" r="5" fill="#34d399" opacity="0.9"/>
  <circle cx="780" cy="75" r="4" fill="#34d399" opacity="0.8"/>
  <circle cx="795" cy="55" r="3" fill="#34d399" opacity="0.7"/>
  <circle cx="805" cy="42" r="3" fill="#34d399" opacity="0.6"/>
  <circle cx="812" cy="33" r="2" fill="#34d399" opacity="0.5"/>
  <circle cx="800" cy="75" r="4" fill="#06b6d4" opacity="0.8"/>
  <circle cx="815" cy="54" r="3" fill="#06b6d4" opacity="0.7"/>
  <circle cx="823" cy="41" r="3" fill="#06b6d4" opacity="0.6"/>
  <circle cx="828" cy="32" r="2" fill="#06b6d4" opacity="0.5"/>
  <circle cx="820" cy="78" r="4" fill="#a78bfa" opacity="0.7"/>
  <circle cx="838" cy="59" r="3" fill="#a78bfa" opacity="0.6"/>
  <circle cx="847" cy="47" r="2" fill="#a78bfa" opacity="0.5"/>
  <circle cx="838" cy="83" r="4" fill="#f472b6" opacity="0.6"/>
  <circle cx="854" cy="68" r="3" fill="#f472b6" opacity="0.5"/>
  <circle cx="862" cy="58" r="2" fill="#f472b6" opacity="0.4"/>
  <circle cx="852" cy="92" r="4" fill="#fb923c" opacity="0.6"/>
  <circle cx="870" cy="82" r="3" fill="#fb923c" opacity="0.5"/>
  <!-- Lines connecting hand landmarks -->
  <line x1="760" y1="100" x2="780" y2="75" stroke="#34d39940" stroke-width="1.5"/>
  <line x1="780" y1="75" x2="795" y2="55" stroke="#34d39940" stroke-width="1"/>
  <line x1="795" y1="55" x2="805" y2="42" stroke="#34d39940" stroke-width="1"/>
  <line x1="805" y1="42" x2="812" y2="33" stroke="#34d39940" stroke-width="1"/>
  <line x1="760" y1="100" x2="800" y2="75" stroke="#06b6d440" stroke-width="1.5"/>
  <line x1="800" y1="75" x2="815" y2="54" stroke="#06b6d440" stroke-width="1"/>
  <!-- Mouse cursor -->
  <polygon points="700,130 700,160 710,153 714,165 720,162 716,150 728,150" fill="#34d399" opacity="0.7"/>
  <!-- Bounding box -->
  <rect x="690" y="25" width="190" height="155" rx="4" fill="none" stroke="#34d39930" stroke-width="1" stroke-dasharray="4,4"/>
  <!-- Title -->
  <text x="50" y="85" font-family="'Trebuchet MS', sans-serif" font-size="32" font-weight="bold" fill="url(#acc3)">Hand-Controlled</text>
  <text x="50" y="128" font-family="'Trebuchet MS', sans-serif" font-size="32" font-weight="bold" fill="url(#acc3)">Mouse</text>
  <text x="50" y="163" font-family="monospace" font-size="12" fill="#6b7280">OpenCV · MediaPipe · PyAutoGUI · Real-time CV</text>
</svg>

# Hand-Controlled Mouse

> **Control your mouse entirely with hand gestures — a real-time computer vision interface built with OpenCV, MediaPipe, and PyAutoGUI**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Google-0F9D58?style=flat-square)](https://mediapipe.dev)
[![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Mouse%20Control-FF6B35?style=flat-square)](https://pyautogui.readthedocs.io)
[![Real-time](https://img.shields.io/badge/Real--time-30fps-22c55e?style=flat-square)]()
[![Status](https://img.shields.io/badge/Status-Complete-22c55e?style=flat-square)]()

</div>

---

## Overview

**Hand-Controlled Mouse** is a touchless human-computer interaction system that replaces physical mouse input with natural hand gestures, captured in real-time via a standard webcam. The project combines Google's MediaPipe hand landmark detection with OpenCV's video processing pipeline and PyAutoGUI's system-level control API to map 21 hand keypoints to precise cursor movements and click actions.

This is a compelling demonstration of applied computer vision — no special hardware needed, just a webcam and Python.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   Hand-Controlled Mouse System                  │
│                                                                 │
│  ┌────────────┐    ┌──────────────┐     ┌─────────────────────┐ │
│  │  Webcam    │───▶│  OpenCV      │───▶│  MediaPipe          │ │
│  │  Feed      │    │  Frame Grab  │     │  Hand Landmark Det. │ │
│  └────────────┘    └──────────────┘     └────────┬────────────┘ │
│                                                  │              │
│                         21 Keypoints (x, y, z)   │              │
│                                                  ▼              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Gesture Interpretation Layer               │    │
│  │   Index Up → Move   |  Pinch → Click  |  Fist → Hold    │    │
│  └───────────────────────────────┬─────────────────────────┘    │
│                                  │                              │
│                                  ▼                              │
│                         ┌────────────────┐                      │
│                         │  PyAutoGUI     │                      │
│                         │  System Mouse  │                      │
│                         └────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Gesture Controls

| Gesture | Action |
|---|---|
| ☝️ Index finger up | Move cursor |
| 🤏 Pinch (index + thumb) | Left click |
| ✌️ Two fingers up | Right click |
| ✊ Closed fist | Click and hold / drag |
| 🖐️ Open palm | Scroll |

---

## Key Features

- **Real-time 30fps tracking** with minimal latency
- **21-point hand skeleton** from MediaPipe for sub-pixel gesture accuracy
- **Smooth cursor motion** using coordinate smoothing to eliminate jitter
- **Multiple gesture actions** — move, click, right-click, drag, and scroll
- **No special hardware** — works with any standard USB or built-in webcam
- **Screen-space mapping** — hand position maps to full display resolution

---

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.9+ |
| Computer Vision | OpenCV 4.x |
| Hand Detection | MediaPipe |
| Mouse Control | PyAutoGUI |
| Math Utils | NumPy |

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/Akshat-C-Kulkarni/Hand-Controlled-Mouse.git
cd Hand-Controlled-Mouse

# Install dependencies
pip install -r requirements.txt

# Run the application
python hand_mouse.py
```

> Make sure your webcam is accessible and well-lit for best results.

---

## Requirements

```
opencv-python
mediapipe
pyautogui
numpy
```

---

## How It Works

1. **Frame Capture** — OpenCV captures video frames from the webcam at 30fps
2. **Landmark Detection** — MediaPipe detects 21 3D hand keypoints per frame
3. **Gesture Classification** — Finger state logic classifies the current gesture
4. **Coordinate Mapping** — Index fingertip position maps to screen coordinates
5. **Action Execution** — PyAutoGUI executes the corresponding mouse action

---

## Author

**Akshat C. Kulkarni**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/akshatckulkarni)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=flat-square&logo=github)](https://github.com/Akshat-C-Kulkarni)

---

<div align="center"><sub>Built with Python · OpenCV · MediaPipe · PyAutoGUI</sub></div>
