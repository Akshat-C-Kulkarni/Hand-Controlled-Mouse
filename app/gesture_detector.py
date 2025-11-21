# app/gesture_detector.py

"""
Gesture detector with explicit scroll_up gesture.
Scroll_down is detected in hand_tracking based on Y positions.
"""

def is_finger_up(landmarks, tip_id, pip_id):
    tip = landmarks[tip_id]
    pip = landmarks[pip_id]
    return tip.y < pip.y

def is_thumb_up(landmarks):
    thumb_tip = landmarks[4]
    thumb_ip  = landmarks[3]
    return thumb_tip.x < thumb_ip.x

def get_finger_states(landmarks):
    return {
        "thumb":  is_thumb_up(landmarks),
        "index":  is_finger_up(landmarks, 8, 6),
        "middle": is_finger_up(landmarks, 12, 10),
        "ring":   is_finger_up(landmarks, 16, 14),
        "pinky":  is_finger_up(landmarks, 20, 18)
    }

def detect_gesture(landmarks, prev_state=None):

    fs = get_finger_states(landmarks)

    thumb  = fs["thumb"]
    index  = fs["index"]
    middle = fs["middle"]
    ring   = fs["ring"]
    pinky  = fs["pinky"]

    # NONE
    if not thumb and not index and not middle and not ring and not pinky:
        return {"gesture": "none", "data": fs}

    # MOVE (all up)
    if thumb and index and middle and ring and pinky:
        return {"gesture": "move", "data": fs}

    # LEFT CLICK = index down only
    if not index and thumb and middle and ring and pinky:
        return {"gesture": "left_click", "data": fs}

    # RIGHT CLICK = ring down only
    if thumb and index and middle and not ring and pinky:
        return {"gesture": "right_click", "data": fs}

    # SCROLL UP = index & middle up, ring+pinky+thumb down
    if index and middle and (not ring) and (not pinky) and (not thumb):
        return {"gesture": "scroll_up", "data": fs}

    # SCROLL DOWN is NOT detected here.
    # It is computed in hand_tracking.py based on Y positions.
    return {"gesture": "unknown", "data": fs}
