import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import logging
import threading
from pynput import mouse, keyboard
from datetime import datetime
import pyautogui

from recorder import Recorder
from replayer import Replayer

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.state_file = "app_state.json"
        self.recorder = Recorder(self)
        self.replayer = Replayer(self)
        
        # Carica lo stato salvato all'avvio
        self.load_state()
        self.setup_ui()

        # Imposta il timer per chiudere la demo
        # self.demo_duration = 600000  # 10 minuti in millisecondi
        # self.root.after(self.demo_duration, self.demo_expired)

    def demo_expired(self):
        """Mostra un messaggio di avviso e chiude l'applicazione dopo il tempo della demo."""
        messagebox.showinfo("Demo Scaduta", "Il periodo di prova è terminato. Grazie per aver provato la demo!")
        self.on_close()

    def setup_ui(self):
        # Configura la GUI
        self.root.title("Autoclicker/Mouse Simulator by TSEKOS")
        self.root.configure(bg="light blue")
        
        tk.Label(self.root, text="Cartella di salvataggio:").grid(row=0, column=0, padx=10, pady=10)
        self.folder_entry = tk.Entry(self.root, width=70)
        self.folder_entry.grid(row=0, column=1)
        tk.Button(self.root, text="Scegli Cartella", command=self.choose_folder).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self.root, text="Nome del file:").grid(row=1, column=0, padx=10, pady=10)
        self.file_entry = tk.Entry(self.root, width=20)
        self.file_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Numero di loop:").grid(row=2, column=0, padx=10, pady=10)
        self.loop_entry = tk.Entry(self.root, width=5)
        self.loop_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Ritardo tra i loop (s):").grid(row=3, column=0, padx=10, pady=10)
        self.delay_entry = tk.Entry(self.root, width=5)
        self.delay_entry.grid(row=3, column=1)

        # Carica i valori salvati nei campi
        self.load_ui_fields()

        # Log display
        self.log_text = tk.Text(self.root, height=10, width=80)
        self.log_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

        # Pulsanti di controllo
        tk.Button(self.root, text="Avvia Registrazione", command=self.recorder.start_recording).grid(row=5, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Riproduci", command=self.replayer.replay_click_path).grid(row=5, column=1, padx=10, pady=10)
        tk.Label(self.root, text="premere <<ESC>> da Keyboard per fermare registrazione", font=("Arial", 8), fg="RED").grid(row=4, column=0, padx=10, pady=(0, 5))
        tk.Button(self.root, text="Esci", command=self.on_close).grid(row=5, column=2, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Salva lo stato alla chiusura

    def add_log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        logging.debug(f"Log aggiornato: {message}")

    def choose_folder(self):
        folder_selected = filedialog.askdirectory()
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, folder_selected)

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                self.state = json.load(f)
        else:
            self.state = {
                "folder": "",
                "filename": "",
                "num_loops": "1",
                "loop_delay": "1"
            }

    def save_state(self):
        """Aggiorna e salva lo stato in app_state.json."""
        try:
            self.state["folder"] = self.folder_entry.get()
            self.state["filename"] = self.file_entry.get()
            self.state["num_loops"] = self.loop_entry.get()
            self.state["loop_delay"] = self.delay_entry.get()
            with open(self.state_file, "w") as f:
                json.dump(self.state, f, indent=4)
            print("Stato salvato correttamente.")
        except Exception as e:
            print(f"Errore durante il salvataggio dello stato: {e}")

    def load_ui_fields(self):
        self.folder_entry.insert(0, self.state.get("folder", ""))
        self.file_entry.insert(0, self.state.get("filename", ""))
        self.loop_entry.insert(0, self.state.get("num_loops", "1"))
        self.delay_entry.insert(0, self.state.get("loop_delay", "1"))

    def on_close(self):
        self.save_state()
        self.root.destroy()



# Avvio dell'applicazione
root = tk.Tk()
app = AutoClickerApp(root)
root.mainloop()
