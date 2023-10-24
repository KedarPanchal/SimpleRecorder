import mouse
import keyboard
import time
import PySimpleGUI as gui
from threading import Thread
from operator import attrgetter

color1 = "#3B503D"
color2 = "#C8CF94"

terminator = "f8"
event = None
mouse_events = []
keyboard_events = []
is_recording = False

def events_fn(window: gui.Window) -> None:
    # This is awful and should not exist
    global terminator
    global event
    global mouse_events
    global keyboard_events
    global is_recording

    record_thread = None
    while True:
        event, values = window.read()
        
        if event == gui.WIN_CLOSED or event == "Exit":
            return
        elif event == "Clear Recording" and not is_recording:
            mouse_events = []
            keyboard_events = []
            window["RECORD_OUTPUT"].update("No recording")
        elif event == "Record":
            if not is_recording:
                is_recording = True
                window["Record"].update(button_color=f"{color1} on {color2}")
                window["RECORD_OUTPUT"].update("Recording...")
                terminator = "f8" if not values[0] else values[0]
                event = ""
                record_thread = Thread(target= lambda : record_fn(window))
                record_thread.start()
            else:
                is_recording = False
                del mouse_events[len(mouse_events) - 1]
                del mouse_events[len(mouse_events) - 1]

        elif event == "Run" and not is_recording:
            window["Run"].update(button_color=f"{color1} on {color2}")
            window["ACTIVITY"].update("Running...")
            
            for _ in range(1 if not check_parse(values[2]) or int(values[2])  < 0 else int(values[2])):
                play_inputs(1 if not check_parse(values[3]) or float(values[3]) < 0 else float(values[3]))
            
            window["Run"].update(button_color=f"{color2} on {color1}")
            window["ACTIVITY"].update("Execution completed")

def record_fn(window: gui.Window) -> None:
    # This is awful and should not exist
    global terminator
    global event
    global mouse_events
    global keyboard_events
    global is_recording

    mouse_events = []
    keyboard_events = []

    mouse.hook(lambda x : accurate_record(mouse_events, x))
    keyboard.hook(lambda x : keyboard_events.append(x))
    last_key = "" if len(keyboard_events) == 0 else keyboard_events[len(keyboard_events) - 1].name
    while event != "Record" and event != "Exit" and event != gui.WIN_CLOSED and last_key != terminator:
        last_key = "" if len(keyboard_events) == 0 else keyboard_events[len(keyboard_events) - 1].name

    if last_key == terminator:
        del keyboard_events[len(keyboard_events) - 1]
        
    mouse.unhook_all()
    keyboard.unhook_all()
    is_recording = False

    window["Record"].update(button_color=f"{color2} on {color1}")
    window["RECORD_OUTPUT"].update("Input recorded")
            
    return

def accurate_record(mouse_arr: list, m_event) -> None:
    if isinstance(m_event, mouse.MoveEvent):
        mouse_arr.append(mouse.MoveEvent(*(mouse.get_position()), m_event.time))
    else:
        mouse_arr.append(m_event)

def check_parse(x: str) -> bool:
    try:
        float(x)
    except(ValueError):
        return False
    else:
        return True

def play_inputs(speed: float):
    global mouse_events
    global keyboard_events

    all_events = mouse_events + keyboard_events
    all_events = sorted(all_events, key=attrgetter("time"))

    state = keyboard.stash_state()
    last_time = all_events[0].time

    for event in all_events:
        if speed > 0:
            time.sleep((event.time - last_time)/speed)
        last_time = event.time

        if isinstance(event, keyboard.KeyboardEvent):
            key = event.scan_code or event.name
            keyboard.press(key) if event.event_type == keyboard.KEY_DOWN else keyboard.release(key)
        elif isinstance(event, mouse.ButtonEvent):
            mouse.press(event.button) if event.event_type == mouse.DOWN else mouse.release(event.button)
        elif isinstance(event, mouse.MoveEvent):
            mouse.move(event.x, event.y)
        elif isinstance(event, mouse.WheelEvent):
            mouse.wheel(event.delta)
    
    keyboard.restore_modifiers(state)

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
