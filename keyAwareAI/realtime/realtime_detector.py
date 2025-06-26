import time
import os
import sys
import joblib
from pynput import keyboard
from utils.feature_extractor import extract_features
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.feature_extractor import extract_features

# Load AI model
model = joblib.load("ml/keylogger_model.joblib")

# Temp log file
LOG_FILE = "data/temp_log.txt"
os.makedirs("data", exist_ok=True)

# Clear previous logs
open(LOG_FILE, "w").close()

# Lock for thread-safe logging
log_lock = threading.Lock()

# Write key and timestamp to file
def write_key(key):
    try:
        with log_lock:
            with open(LOG_FILE, "a") as f:
                f.write(f"{key.char if hasattr(key, 'char') else str(key)} {time.time()}\n")
    except Exception:
        pass  # Ignore untypable keys

# Monitor keys
def on_press(key):
    write_key(key)

# Background analysis loop
def analyze_behavior_loop():
    while True:
        time.sleep(10)  # Analyze every 10 seconds

        # Thread-safe read
        with log_lock:
            try:
                features = extract_features(LOG_FILE)
                if features:
                    prediction = model.predict([features])[0]
                    if prediction == 1:
                        print("Suspicious behavior detected! [Potential keylogger]")
                    else:
                        print("Normal typing behavior")
                else:
                    print("Not enough keystrokes yet.")
            except Exception as e:
                print(f"Error during analysis: {e}")

# Start analyzer in background
threading.Thread(target=analyze_behavior_loop, daemon=True).start()

# Start keylogger
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
