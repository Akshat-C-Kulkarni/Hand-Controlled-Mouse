# app/gesture_detector.py

"""
Gesture detector using simple finger-state rules (no pinch detection).
Includes 2-second logging delay.
"""

import time

# 2-second delay for gesture logging
_last_logged_time = 0


# ---------------------------------------------------
# Finger Up/Down Detection
# ---------------------------------------------------
def is_finger_up(landmarks, tip_id, pip_id):
    """
    Returns True if the fingertip is ABOVE the PIP joint (y smaller).
    """
    tip = landmarks[tip_id]
    pip = landmarks[pip_id]
    return tip.y < pip.y


def is_thumb_up(landmarks):
    """
    Thumb is considered 'up' if its x-position is LEFT of its joint
    when the frame is flipped (mirror view).
    """
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    return thumb_tip.x < thumb_ip.x


def get_finger_states(landmarks):
    """
    Returns a dictionary of finger up/down states.
    """
    return {
        "thumb":  is_thumb_up(landmarks),
        "index":  is_finger_up(landmarks, 8, 6),
        "middle": is_finger_up(landmarks, 12, 10),
        "ring":   is_finger_up(landmarks, 16, 14),
        "pinky":  is_finger_up(landmarks, 20, 18)
    }


# ---------------------------------------------------
# Gesture Detection (Based on Your New Patterns)
# ---------------------------------------------------
def detect_gesture(landmarks, prev_state=None):
    """
    Returns:
      {"gesture": <str>, "data": ...}

    New gesture rules:
    -------------------------------------
    none        : all fingers DOWN
    move        : all fingers UP
    left_click  : index DOWN, rest UP
    right_click : ring DOWN, rest UP
    scroll      : index & middle UP, rest DOWN
    -------------------------------------
    """

    global _last_logged_time
    now = time.time()

    # ------------- 2-second delay ---------------
    if now - _last_logged_time < 2:
        return {"gesture": "wait", "data": None}
    _last_logged_time = now
    # --------------------------------------------

    finger_states = get_finger_states(landmarks)

    thumb   = finger_states["thumb"]
    index   = finger_states["index"]
    middle  = finger_states["middle"]
    ring    = finger_states["ring"]
    pinky   = finger_states["pinky"]

    # ---------- Your NEW Rules ----------

    # 1. None: All fingers DOWN
    if not thumb and not index and not middle and not ring and not pinky:
        return {"gesture": "none", "data": finger_states}

    # 2. Move: ALL fingers UP
    if thumb and index and middle and ring and pinky:
        return {"gesture": "move", "data": finger_states}

    # 3. Left Click: ONLY index DOWN (others UP)
    if thumb and not index and middle and ring and pinky:
        return {"gesture": "left_click", "data": finger_states}

    # 4. Right Click: ONLY ring DOWN (others UP)
    if thumb and index and middle and not ring and pinky:
        return {"gesture": "right_click", "data": finger_states}

    # 5. Scroll: Index & Middle UP, rest DOWN
    if (not thumb) and index and middle and (not ring) and (not pinky):
        return {"gesture": "scroll", "data": {"index": index, "middle": middle}}

    # Otherwise unknown
    return {"gesture": "unknown", "data": finger_states}
