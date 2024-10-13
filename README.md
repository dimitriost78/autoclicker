# autoclicker
python autoclicker

# AutoClickerApp

AutoClickerApp is a Python application for recording and replaying mouse and keyboard actions. It allows you to record clicks and keyboard inputs, save them in a JSON file, and replay the recorded actions. The app is designed to automatically execute sequences of actions repeated


## Features
- **Click Recording**: Records mouse clicks and keyboard inputs along with any delays.
- **Replay Recorded Actions**: Executes the recorded clicks and scrolls, with support for loops.
- **Graphical Interface**: Easy to use, with buttons to start/stop recording and replay actions.
- **JSON Saving**: Saves click and input sequences in JSON format for later use.


## Prerequisiti

Ensure you have Python 3.6 or above installed. Additionally, the project uses the following libraries:

- `tkinter` (included in Python for creating GUIs)
- `pynput` (to listen to and simulate mouse and keyboard events)
- `pyautogui` (to simulate mouse clicks and keystrokes)

To install additional dependencies, you can use `pip`:

```bash
pip install pynput pyautogui
```
Esegui l'applicazione:

```bash
python autoClickerApp.py
```
## Usage
- `Start Recording`:

Click Start Recording to begin recording clicks and keyboard inputs. The numbers entered on the keyboard are saved for each click.

- `Stop Recording`:

Press Esc to stop recording. The actions are saved in a JSON file in the specified folder.

- `Replay Actions`:

Click Play to execute the recorded sequence of actions. 

- `Close the Application`:

Use the Exit button to close the application.

## License
This project is distributed under the MIT License. See the LICENSE file for more details.