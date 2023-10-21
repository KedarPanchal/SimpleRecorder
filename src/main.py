import PySimpleGUI as gui
from threading import Thread
from lib import events_fn, record_fn

def main() -> None:
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
    
    events_fn(window)

    window.close()

if __name__ == '__main__':
    main()
