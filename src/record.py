import mouse
import keyboard
import time
from threading import Thread

""" 
Records inputs until a terminator key is pressed. Stores these recorded inputs inside two arrays for both mouse and keyboard inputs and returns a tuple of these events
terminator: the name of the key that terminates the recording
returns: a tuple containing an array of the mouse events and an array of the keyboard events
"""
def record_inputs(terminator: str="f8"):
    mouse_events = []
    keyboard_events = []

    mouse.hook(lambda x : accurate_record(mouse_events, x))

    keyboard_events = keyboard.record(terminator)
    mouse.unhook_all()
    del keyboard_events[len(keyboard_events) - 1]
    return (mouse_events, keyboard_events)

"""
Changes the position of a mouse event to accurately reflect its position on the screen then appends it to a list of mouse events
mouse_arr: the list of mouse events to pass the accurately position mouse event into
event: the mouse event whose position needs to be changed to be accurate
"""
def accurate_record(mouse_arr, event):
    if isinstance(event, mouse.MoveEvent):
        mouse_arr.append(mouse.MoveEvent(*(mouse.get_position()), event.time))
    else:
        mouse_arr.append(event)

"""
Plays the inputs from a list of mouse events and keyboard events simultaneously at a certain speed
mouse_events: the list of mouse events to play
keyboard_events: the list of keyboard events to play
speed: the speed at which these events should be played (1x speed is the default)
"""
def play_inputs(mouse_events: list, keyboard_events:list, speed: float=1):
    print(keyboard_events)
    keyboard.start_recording()
    keyboard.stop_recording()
    mouse_thread = Thread(target=lambda : mouse.play(events=mouse_events, speed_factor=speed))
    keyboard_thread = Thread(target=lambda : keyboard_play(events=keyboard_events, start_time=min(mouse_events[0].time, keyboard_events[0].time), speed_factor=speed))

    mouse_thread.start()
    keyboard_thread.start()

    mouse_thread.join()
    keyboard_thread.join()

"""
Plays the keypresses in an array of keyboard events. Resets the state of the keyboard when the function is called and restores it afterward
events: the list of keypresses to play
start_time: the time that the first keypress or mouse event occurred
speed_factor: the speed at which these keypresses should be played (1x speed is the default)
"""
def keyboard_play(events: list, start_time, speed_factor: float=1):
    state = keyboard.stash_state()
    last_time = start_time
    
    for event in events:
        if speed_factor > 0:
            time.sleep((event.time - last_time)/speed_factor)
        last_time = event.time

        key = event.scan_code or event.name
        keyboard.press(key) if event.event_type == keyboard.KEY_DOWN else keyboard.release(key)
        
    keyboard.restore_modifiers(state)
