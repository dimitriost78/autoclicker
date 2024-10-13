import time
from tkinter import messagebox
import json
import pyautogui
import threading
import os

class Replayer:
    def __init__(self, app):
        self.app = app

    def load_click_path(self, record_file):
        try:
            with open(record_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            self.app.add_log_message(f"Errore di caricamento: {e}")
            return []

    def replay_click_path(self):
        threading.Thread(target=self.execute_replay).start()

    def execute_replay(self):
        folder = self.app.folder_entry.get()
        filename = self.app.file_entry.get() + ".json"
        
        if not folder or not filename:
            messagebox.showerror("Errore", "Per favore, seleziona una cartella e inserisci un nome file.")
            return

        record_file = os.path.join(folder, filename)
        clicks_and_delays = self.load_click_path(record_file)
        num_loops = int(self.app.loop_entry.get())
        loop_delay = float(self.app.delay_entry.get())
        
        self.app.add_log_message("******************** Inizio riproduzione ********************")
        
        for loop in range(num_loops):
            if loop < num_loops:
                self.app.add_log_message(f"--- Loop {loop + 1}/{num_loops} ---")
                for event in clicks_and_delays:
                    x, y, event_type, text = event['x'], event['y'], event['type'], event.get('text', '0')
                    if event_type == "click":
                        pyautogui.moveTo(x, y, duration=0.4)
                        pyautogui.click()
                        if event.get("text", ""):
                            pyautogui.typewrite(event['text'], interval=0.1)
                    elif event_type == "scroll":
                        pyautogui.scroll(event['dy'], x=x, y=y)
                    self.app.add_log_message(f"Evento {event_type} con : {x},{y} con valore {text}")
                    time.sleep(event['delay'])
                time.sleep(loop_delay)
        self.app.add_log_message("************ Fine riproduzione **********")
