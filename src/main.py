from lib import *
import PySimpleGUI as gui
import mouse
import keyboard

gui.theme("DarkGreen2")
layout = [
    [gui.Text("End Recording Key: "), gui.InputText()],
    [gui.Push(), gui.Button("Record"), gui.Text("No recording", key="RECORD_OUTPUT"), gui.Push()],
    [gui.HorizontalSeparator(pad=(10, 10))],
    [gui.Text("Number of Executions: "), gui.InputText()],
    [gui.Push(), gui.Text("Speed: "), gui.InputText()],
    [gui.Push(), gui.Button("Run"), gui.Text("Inactive", key="ACTIVITY"), gui.Push()],
    [gui.HorizontalSeparator(pad=(10, 10))],
    [gui.Push(), gui.Button("Exit"), gui.Button("Clear Recording"), gui.Push()]
]

window = gui.Window(title="Simple Recorder", layout=layout, element_justification='l', icon="C:/Users/kedar/00_Kedar/Python Projects/SimpleRecorder/out/imgs/SimpleRecorder.ico", titlebar_icon="C:/Users/kedar/00_Kedar/Python Projects/SimpleRecorder/out/imgs/SimpleRecorder.ico")

mouse_inputs = []
keyboard_inputs = []
is_recording = False

while True:
    event, values = window.read()

    if event == gui.WIN_CLOSED or event == "Exit":
        break
    if not is_recording:
        if event == "Record":
            is_recording = True
            try:
                mouse_inputs, keyboard_inputs = record_inputs() if not values[0] else record_inputs(values[0])
                window["RECORD_OUTPUT"].update("Input recorded successfully")
            except ValueError:
                window["RECORD_OUTPUT"].update("Input was unable to be recorded")
                continue
            finally:
                is_recording = False
        elif event == "Clear Recording":
            mouse_inputs = keyboard_inputs = []
            window["RECORD_OUTPUT"].update("No recording")
        elif event == "Run":
            try:
                speed_factor = float(values[3]) if check_parse(values[3]) else 1
                window["ACTIVITY"].update("Running...")
                for i in range((1 if (not check_parse(values[2]) or int(values[2]) < 1) else int(values[2]))):
                    play_inputs(mouse_events=mouse_inputs, keyboard_events=keyboard_inputs, speed=speed_factor)
                window["ACTIVITY"].update("Execution completed")
            except ValueError:
                play_inputs(mouse_events=mouse_inputs, keyboard_events=keyboard_inputs)
                window["ACTIVITY"].update("Execution completed")

mouse.unhook_all()
keyboard.unhook_all()
window.close()