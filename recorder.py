import json
import time
from tkinter import messagebox
from pynput import mouse, keyboard
from datetime import datetime
import threading
import os


class Recorder:
    def __init__(self, app):
        self.app = app
        self.clicks_and_delays = []
        self.last_click_time = datetime.now()
        self.recording = False
        self.typing = ""
        self.stop_recording_flag = False
        self.record_file = ""

    def start_recording(self):
        self.recording = True
        self.stop_recording_flag = False
        folder = self.app.folder_entry.get()
        filename = self.app.file_entry.get() + ".json"

        if not folder or not filename:
            messagebox.showerror("Error", "the folder's path and file's name must NOT be empty.")
            return

        self.record_file = os.path.join(folder, filename)
        self.clicks_and_delays.clear()
        self.last_click_time = datetime.now()

        self.app.add_log_message("******* Started recording *******")

        # Avvia i listener in un thread separato
        listener_thread = threading.Thread(target=self.run_listeners)
        listener_thread.start()

    def run_listeners(self):
        # Usa `listener` come variabili d'istanza per fermarli da altri metodi
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press_key, on_release=self.on_press_stop)

        # Avvia entrambi i listener
        self.mouse_listener.start()
        self.keyboard_listener.start()

        # Controlla finché `stop_recording_flag` non diventa True
        while not self.stop_recording_flag:
            time.sleep(0.1)

        # Ferma i listener quando `stop_recording_flag` è True
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

        # Salva i clic registrati
        self.save_click_path()
        self.app.add_log_message("******* Recording Finished *********")

    def save_click_path(self):
        if self.clicks_and_delays:
            try:
                with open(self.record_file, 'w') as file:
                    json.dump(self.clicks_and_delays, file, indent=4)
                self.app.add_log_message(f"Path saved into {self.record_file}")
            except Exception as e:
                self.app.add_log_message(f"Error on saving: {e}")

    def on_click(self, x, y, button, pressed):
        if pressed and self.recording:
            delay = (datetime.now() - self.last_click_time).total_seconds() if self.last_click_time else 0
            self.clicks_and_delays.append({
                "type": "click",
                "x": x,
                "y": y,
                "delay": delay,
                "text": self.typing
            })
            self.last_click_time = datetime.now()

            # Logga l'evento di clic con o senza testo
            if self.typing:
                self.app.add_log_message(f"Action Clic saved with text value: {self.typing}")
            else:
                self.app.add_log_message("Action Clic saved without text value.")
        
            # Resetta `self.typing` per il prossimo clic
            self.typing = ""

    def on_scroll(self, x, y, dx, dy):
        if self.recording:
            delay = (datetime.now() - self.last_click_time).total_seconds() if self.last_click_time else 0
            self.clicks_and_delays.append({
                "type": "scroll",
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "delay": delay,
                "text": self.typing
            })
            self.last_click_time = datetime.now()
            self.app.add_log_message("Scroll Action saved.")

    def on_press_key(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                self.typing += key.char
        except AttributeError:
            pass

    def on_press_stop(self, key):
        if key == keyboard.Key.esc:
            self.stop_recording_flag = True  # Imposta il flag per fermare la registrazione
            self.app.add_log_message("Recording interrupted by User!.")
    
    def stop_recording_process(self):  # Rinomina il metodo per evitare conflitti
        """Interrompe la registrazione."""
        self.stop_recording_flag = True
