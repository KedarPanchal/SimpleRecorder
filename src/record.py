import time

class Event:
    def __init__(self, time):
        self.time = time

class MouseEvent(Event):
    def __init__(self, time):
        super(time)

class KeyEvent(Event):
    def __init__(self, key, time):
        super(time)
        self.key = key

class KeyPressEvent(KeyEvent):
    def __init__(self, key, time):
        super(time, key)

class KeyReleaseEvent(KeyEvent):
    def __init__(self, key, time):
        super(time, key)

class MouseMoveEvent(MouseEvent):
    def __init__(self, x, y, time):
        super(time)
        self.x = x
        self.y = y

class MouseButtonEvent(MouseEvent):
    def __init__(self, button, time):
        super(time)
        self.button = button

class MouseClickEvent(MouseButtonEvent):
    def __init__(self, button, time):
        super(button, time)

class MouseReleaseEvent(MouseButtonEvent):
    def __init__(self, button, time):
        super(button, time)

class MouseWheelEvent(MouseEvent):
    def __init__(self, deltax, deltay, time):
        super(time)
        self.deltax = deltax
        self.deltay = deltay

def on_move(x, y):
    return MouseMoveEvent(x, y, time.time())

def on_click(button, pressed):
    return MouseClickEvent(button, time.time()) if pressed else MouseReleaseEvent(button, time.time())

def on_scroll(dx, dy):
    return MouseWheelEvent(dx, dy, time.time())

def on_press(key):
    return KeyPressEvent(key, time.time())

def on_release(key):
    return KeyReleaseEvent(key, time.time())