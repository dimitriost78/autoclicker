from tkinter import messagebox
import json
import time
from pynput import mouse, keyboard
from datetime import datetime
import os


class Recorder:
    def __init__(self, app):
        self.app = app
        self.clicks_and_delays = []
        self.last_click_time = datetime.now()
        self.recording = False
        self.typing = ""
        self.stop_recording = False
        self.record_file = ""

    def start_recording(self):
        self.recording = True
        self.stop_recording = False
        folder = self.app.folder_entry.get()
        filename = self.app.file_entry.get() + ".json"

        if not folder or not filename:
            messagebox.showerror("Errore", "Per favore, seleziona una cartella e inserisci un nome file.")
            return

        self.record_file = os.path.join(folder, filename)
        self.clicks_and_delays.clear()
        self.last_click_time = datetime.now()

        self.app.add_log_message("********* Inizio registrazione **********")

        with mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll) as mouse_listener, \
                keyboard.Listener(on_press=self.on_press_key, on_release=self.on_press_stop) as key_listener:
            while not self.stop_recording:
                time.sleep(0.1)
            mouse_listener.stop()
            key_listener.stop()

        self.save_click_path()
        self.app.add_log_message("********* Fine registrazione *********")

    def save_click_path(self):
        if self.clicks_and_delays:
            try:
                with open(self.record_file, 'w') as file:
                    json.dump(self.clicks_and_delays, file, indent=4)
                self.app.add_log_message(f"Percorso salvato in {self.record_file}")
            except Exception as e:
                self.app.add_log_message(f"Errore di salvataggio: {e}")

    def on_click(self, x, y, button, pressed):
        if pressed and self.recording:
            delay = (datetime.now() - self.last_click_time).total_seconds() if self.last_click_time else 0
            self.clicks_and_delays.append({"type": "click", "x": x, "y": y, "delay": delay, "text": self.typing})
            self.last_click_time = datetime.now()
            # self.app.add_log_message(f"Evento click con : {x},{y} con valore {self.typing}")
            if self.typing:
                self.app.add_log_message(f"Clic salvato con testo: {self.typing}")
            else:
                self.app.add_log_message("Clic salvato senza testo.")
        
            # Resetta `self.typing` per il prossimo clic
            self.typing = ""
             # Aggiorna il tempo dell'ultimo clic
            self.last_click_time = datetime.now()

    def on_scroll(self, x, y, dx, dy):
        if self.recording:
            delay = (datetime.now() - self.last_click_time).total_seconds() if self.last_click_time else 0
            self.clicks_and_delays.append({"type": "scroll", "x": x, "y": y, "dx": dx, "dy": dy, "delay": delay, "text": self.typing})
            self.last_click_time = datetime.now()
            # self.app.add_log_message(f"Evento scroll con : {x},{y} con valore {self.typing}")

    def on_press_key(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                self.typing += key.char
        except AttributeError:
            pass

    def on_press_stop(self, key):
        if key == keyboard.Key.esc:
            self.stop_recording = True
    
    def stop_recording(self):
        """Interrompe la registrazione."""
        self.stop_recording = True
        self.app.add_log_message("Registrazione interrotta dall'utente.")

