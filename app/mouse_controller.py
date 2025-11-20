# app/mouse_controller.py

from pynput.mouse import Controller, Button

mouse = Controller()

# Smoothing factor for cursor movement (0–1)
SMOOTHING = 0.2

# Store last position for smoothing
_last_x, _last_y = None, None


def move_cursor(x, y, screen_w, screen_h):
    global _last_x, _last_y

    target_x = int(x * screen_w)
    target_y = int(y * screen_h)

    # Initialize if first move
    if _last_x is None:
        _last_x, _last_y = target_x, target_y

    # Smooth movement
    new_x = int(_last_x + (target_x - _last_x) * SMOOTHING)
    new_y = int(_last_y + (target_y - _last_y) * SMOOTHING)

    mouse.position = (new_x, new_y)

    _last_x, _last_y = new_x, new_y


def left_click():
    mouse.press(Button.left)
    mouse.release(Button.left)


def right_click():
    mouse.press(Button.right)
    mouse.release(Button.right)


def scroll_vertical(delta):
    """delta positive → scroll up, negative → scroll down"""
    mouse.scroll(0, delta)
