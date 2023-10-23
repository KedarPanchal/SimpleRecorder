import time
import PySimpleGUI as gui
from pynput import mouse, keyboard
from threading import Thread
from record import *

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
            
            for i in range(1 if not check_parse(values[2]) or int(values[2])  < 1 else int(values[2])):
                play_inputs(1 if not check_parse(values[3]) or float(values[3]) < 1 else float(values[3]))
            
            window["Run"].update(button_color=f"{color2} on {color1}")
            window["ACTIVITY"].update("Execution completed")

def record_fn(window: gui.Window) -> None:
    global mouse_events
    global keyboard_events
    global event
    global is_recording

    mouse_events = []
    keyboard_events = []

    last_key = ""

    mouse_listener = mouse.Listener(
        on_move=lambda x, y: mouse_events.append(on_move(x, y)),
        on_click=lambda x, y, button, pressed: mouse_events.append(on_click(button, pressed)),                  
        on_scroll=lambda x, y, dx, dy: mouse_events.append(on_scroll(dx, dy)))
    mouse_listener.start()

    keyboard_listener = keyboard.Listener(
        on_press=lambda key : keyboard_events.append(on_press(key)),
        on_release=lambda key : keyboard_events.append(on_release(key))
    )
    keyboard_listener.start()

    while event != "Record" and event != "Exit" and event != gui.WIN_CLOSED and last_key != terminator:
        last_key = keyboard_events[len(keyboard_events) - 1]

    mouse_listener.stop()
    keyboard_listener.stop()
    is_recording = False

    window["Record"].update(button_color=f"{color2} on {color1}")
    window["RECORD_OUTPUT"].update("Input recorded")

    return

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

    mouse_thread = Thread(target=lambda : mouse.play(events=mouse_events, speed_factor=speed))
    keyboard_thread = Thread(target=lambda : keyboard_play(events=keyboard_events, start_time=min(mouse_events[0].time, keyboard_events[0].time), speed_factor=speed))

    mouse_thread.start()
    keyboard_thread.start()

    mouse_thread.join()
    keyboard_thread.join()

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
