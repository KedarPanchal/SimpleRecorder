import mouse
import keyboard
from threading import Thread

def record_inputs(terminator: str="esc"):
    mouse_events = []
    keyboard_events = []

    mouse.hook(lambda x : accurate_record(mouse_events, x))
    keyboard.hook(keyboard_events.append)

    keyboard.wait(terminator)
    mouse.unhook_all()
    keyboard.unhook_all()
    return (mouse_events, keyboard_events)

def accurate_record(mouse_arr, event):
    if isinstance(event, mouse.MoveEvent):
        mouse_arr.append(mouse.MoveEvent(*(mouse.get_position()), event.time))
    else:
        mouse_arr.append(event)

def play_inputs(mouse_events: list, keyboard_events:list, speed: float=1):
    mouse_thread = Thread(target=lambda : mouse.play(events=mouse_events, speed_factor=speed))
    keyboard_thread = Thread(target=lambda : keyboard.play(events=keyboard_events, speed_factor=speed))

    mouse_thread.start()
    keyboard_thread.start()

    mouse_thread.join()
    keyboard_thread.join()
