
import pyautogui
import time
import json
import os
from pynput import mouse, keyboard
from datetime import datetime

clicks_and_delays = []
last_click_time = None
recording = False
typing = ""  
stop_recording = False
record_file = ""
first_click = True
post_scroll_typing = False

# Mapping numpad keys to numbers based on detected KeyCodes
NUMPAD_MAPPING = {
    keyboard.KeyCode.from_vk(96): '0',  # Numpad 0
    keyboard.KeyCode.from_vk(97): '1',  # Numpad 1
    keyboard.KeyCode.from_vk(98): '2',  # Numpad 2
    keyboard.KeyCode.from_vk(99): '3',  # Numpad 3
    keyboard.KeyCode.from_vk(100): '4', # Numpad 4
    keyboard.KeyCode.from_vk(101): '5', # Numpad 5
    keyboard.KeyCode.from_vk(102): '6', # Numpad 6
    keyboard.KeyCode.from_vk(103): '7', # Numpad 7
    keyboard.KeyCode.from_vk(104): '8', # Numpad 8
    keyboard.KeyCode.from_vk(105): '9'  # Numpad 9
}

def on_click(x, y, button, pressed):
    global last_click_time, typing, first_click, post_scroll_typing

    if pressed and recording:
        current_time = datetime.now()
        delay = (current_time - last_click_time).total_seconds() if last_click_time else 0
        last_click_time = current_time

        if first_click:
            delay = 0
            first_click = False

        # Associate typing after scroll events until it is reset
        text_to_save = typing if post_scroll_typing or typing else ""
        clicks_and_delays.append({"type": "click", "x": x, "y": y, "delay": delay, "text": text_to_save})
        print(f"Click at ({x}, {y}), delay {delay}, text '{text_to_save}'")
        
        if post_scroll_typing or typing:
            typing = ""  # Reset typing after it's saved on the next click
            post_scroll_typing = False

def on_scroll(x, y, dx, dy):
    global last_click_time, typing, post_scroll_typing

    if recording:
        current_time = datetime.now()
        delay = (current_time - last_click_time).total_seconds() if last_click_time else 0
        last_click_time = current_time

        clicks_and_delays.append({"type": "scroll", "x": x, "y": y, "dx": dx, "dy": dy, "delay": delay, "text": typing})
        print(f"Scroll at ({x}, {y}), dx={dx}, dy={dy}, delay {delay}, text '{typing}'")
        post_scroll_typing = True  # Activate typing retention post-scroll
        time.sleep(0.2)

def on_press_key(key):
    global typing
    try:
        if hasattr(key, 'char') and key.char is not None:
            typing += key.char  # Add character if it's standard
        elif key in NUMPAD_MAPPING:  # Add character if it's from numpad
            typing += NUMPAD_MAPPING[key]
        elif key == keyboard.Key.space:
            typing += " "
        elif key == keyboard.Key.backspace:
            typing = typing[:-1]
        elif key == keyboard.Key.enter:
            typing += "\n"
    except AttributeError:
        pass

def on_press_stop(key):
    global stop_recording
    if key == keyboard.Key.esc:
        stop_recording = True
        return False

def save_click_path():
    if clicks_and_delays:
        try:
            with open(record_file, 'w') as file:
                json.dump(clicks_and_delays, file, indent=4)
            print(f"Path saved to {record_file}")
        except Exception as e:
            print(f"Error saving: {e}")
    else:
        print("Nothing recorded")

def load_click_path():
    if os.path.exists(record_file):
        try:
            with open(record_file, 'r') as file:
                data = json.load(file)
                print(f"Loaded path: {data}")
                return data
        except Exception as e:
            print(f"Error loading path: {e}")
    else:
        print("Path not found")
    return []

def replay_click_path(clicks_and_delays, num_loops=1, loop_delay=0):
    if not clicks_and_delays:
        print("No events recorded")
        return

    for loop in range(num_loops):
        print(f"Loop {loop + 1}/{num_loops}")
        for event in clicks_and_delays:
            x, y, delay, event_type = event['x'], event['y'], event['delay'], event['type']
            time.sleep(delay)

            if event_type == "click":
                pyautogui.moveTo(x, y, duration=0.5)
                pyautogui.click()
                if event.get("text", ""):
                    pyautogui.typewrite(event['text'], interval=0.1)
                    time.sleep(0.5)
            elif event_type == "scroll":
                pyautogui.scroll(event['dy'], x=x, y=y)

        if loop < num_loops - 1:
            time.sleep(loop_delay)

def start_recording():
    global recording, last_click_time, stop_recording, first_click, post_scroll_typing
    last_click_time = None
    clicks_and_delays.clear()
    recording = True
    stop_recording = False
    first_click = True
    post_scroll_typing = False

    with mouse.Listener(on_click=on_click, on_scroll=on_scroll) as mouse_listener,          keyboard.Listener(on_press=on_press_key) as keyboard_listener,          keyboard.Listener(on_press_stop) as stop_listener:
        while not stop_recording:
            time.sleep(0.1)
        mouse_listener.stop()
        keyboard_listener.stop()
        stop_listener.stop()

    save_click_path()

def main():
    global record_file
    while True:
        mode = input("Enter 'r' to record, 'p' to play, or 'q' to quit: ").strip().lower()

        if mode == 'r':
            record_file = input("Enter filename to save recording: ").strip()
            start_recording()
        elif mode == 'p':
            record_file = input("Enter filename to load: ").strip()
            path = load_click_path()
            if path:
                try:
                    num_loops = int(input("Enter loop count: ").strip())
                    loop_delay = float(input("Enter delay between loops: ").strip())
                    replay_click_path(path, num_loops=num_loops, loop_delay=loop_delay)
                except ValueError:
                    print("Invalid input")
        elif mode == 'q':
            break

if __name__ == "__main__":
    main()
