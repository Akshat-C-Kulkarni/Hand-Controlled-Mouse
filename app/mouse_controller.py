# app/mouse_controller.py

from pynput.mouse import Controller, Button

mouse = Controller()

SMOOTH_ALPHA = 0.25
LARGE_MOVE_THRESHOLD_PX = 500

_last_x, _last_y = None, None

def move_cursor(x, y, screen_w, screen_h):
    global _last_x, _last_y

    x = max(0.0, min(1.0, x))
    y = max(0.0, min(1.0, y))

    tx = int(x * screen_w)
    ty = int(y * screen_h)

    if _last_x is None:
        _last_x, _last_y = tx, ty
        mouse.position = (tx, ty)
        return

    if abs(tx - _last_x) > LARGE_MOVE_THRESHOLD_PX or abs(ty - _last_y) > LARGE_MOVE_THRESHOLD_PX:
        _last_x, _last_y = tx, ty
        mouse.position = (tx, ty)
        return

    new_x = int(_last_x + (tx - _last_x) * SMOOTH_ALPHA)
    new_y = int(_last_y + (ty - _last_y) * SMOOTH_ALPHA)

    mouse.position = (new_x, new_y)
    _last_x, _last_y = new_x, new_y

def reset_smoothing_state():
    global _last_x, _last_y
    _last_x, _last_y = None, None

def left_click():
    mouse.press(Button.left)
    mouse.release(Button.left)

def right_click():
    mouse.press(Button.right)
    mouse.release(Button.right)

def scroll_vertical(delta):
    mouse.scroll(0, delta)
