import time
from tkinter import messagebox
import json
import pyautogui
import threading
import os
from pynput import keyboard

class Replayer:
    def __init__(self, app):
        self.app = app
        self.stop_playback_flag = False

    def load_click_path(self, record_file):
        try:
            with open(record_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            self.app.add_log_message(f"Error on loading: {e}")
            return []

    def replay_click_path(self):
        threading.Thread(target=self.execute_replay).start()
        threading.Thread(target=self.run_listeners).start()
    
    def on_press_stop(self, key):
        if key == keyboard.Key.esc:
            self.stop_playback_flag = True  # Imposta il flag per fermare la registrazione
            self.app.add_log_message("Palyback interrupted by User!.")

    def run_listeners(self):
            # Usa `listener` come variabili d'istanza per fermarli da altri metodi

            self.keyboard_listener = keyboard.Listener(on_release=self.on_press_stop)

            # Avvia entrambi i listener
            self.keyboard_listener.start()

            # Controlla finché `stop_recording_flag` non diventa True
            while not self.stop_playback_flag:
                time.sleep(0.1)

            # Ferma i listener quando `stop_recording_flag` è True
            self.keyboard_listener.stop()

            # Salva i clic registrati
            self.app.add_log_message("******* Playback Stoped *********")


    def execute_replay(self):
        folder = self.app.folder_entry.get()
        filename = self.app.file_entry.get() + ".json"
        self.stop_playback_flag = False
        if not folder or not filename:
            messagebox.showerror("Errore", "Per favore, seleziona una cartella e inserisci un nome file.")
            return

        record_file = os.path.join(folder, filename)
        clicks_and_delays = self.load_click_path(record_file)
        num_loops = int(self.app.loop_entry.get())
        loop_delay = float(self.app.delay_entry.get())
        
        self.app.add_log_message("******** Simulation Started ********")
        
        for loop in range(num_loops):
            if loop < num_loops:
                self.app.add_log_message(f"--- Loop {loop + 1}/{num_loops} ---")
                if self.stop_playback_flag:
                    break
                for event in clicks_and_delays:
                    if self.stop_playback_flag:
                        break
                    x, y, event_type, text = event['x'], event['y'], event['type'], event.get("text", "")
                    log_text = text if text else "N/A"
                    if event_type == "click":
                        self.esegui_moveto_solo_se_differente(x, y)
                        if event.get("text", ""):
                            pyautogui.typewrite(event['text'], interval=0.1)
                    elif event_type == "scroll":
                        pyautogui.scroll(event['dy'], x=x, y=y)
                    self.app.add_log_message(f"Event {event_type} with : {x},{y} with text value: {log_text}")
                    time.sleep(event['delay'])
                time.sleep(loop_delay)
        self.stop_playback_flag ==False
        self.app.add_log_message("******** Simulation ended *******")


    def esegui_moveto_solo_se_differente(self,x, y):
        # Ottieni la posizione corrente del mouse
        posizione_corrente = pyautogui.position()
        posizione_x, posizione_y = posizione_corrente

        # Verifica se le coordinate di destinazione sono diverse da quelle attuali
        if posizione_x != x or posizione_y != y:
            pyautogui.moveTo(x, y, duration=0.4)
        pyautogui.click()  # Esegui comunque il click