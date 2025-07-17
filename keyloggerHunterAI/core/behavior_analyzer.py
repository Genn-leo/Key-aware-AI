import os
import time
import threading
import joblib
from pynput import keyboard 
from core.logger import log_alert

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ai", "behavior_model.joblib"))
KEYLOG_FILE = "data/temp_log.txt"
LEARNING_FILE = "data/learning_samples.csv"

model = joblib.load(MODEL_PATH)
log_lock = threading.Lock()

# Make sure the files exist
os.makedirs("data", exist_ok=True)
open(KEYLOG_FILE, "w").close()
if not os.path.exists(LEARNING_FILE):
    with open(LEARNING_FILE, "w") as f:
        f.write("avg_delay,burst_ratio,total_keys,unique_keys,label\n")
    
def extract_features(file_path):
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        if len(lines) < 5:
            return None
        
        timestamps = []
        keys = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >=2:
                key, t = parts[0], float(parts[1])
                keys.append(key)
                timestamps.append(t)
        
        if len(timestamps) < 2:
            return None
        
        delays = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
        avg_delay = sum(delays) / len(delays)
        burst_ratio = len([d for d in delays if d < 0.1]) / len(delays)
        total_keys = len(keys)
        unique_keys = len(set(keys))

        return [avg_delay, burst_ratio, total_keys, unique_keys]
    except Exception as e:
        print(f"[Feature Extraction Error] {e}")
        return None

def analyze_typing():
    while True:
        time.sleep(10)

        with log_lock:
            features = extract_features(KEYLOG_FILE)
            if features:
                try:
                    prediction = model.predict([features])[0]
                    if prediction == 1:
                        log_alert("AI flagged suspicious typing behaviour!")
                        save_learning_sample(features)
                    else:
                        print("Typing behaviour normal.")
                except Exception as e:
                    print(f"[Prediction Error] {e}")
            else:
                print("Waiting for more Keystrokes...")

def save_learning_sample(features):
    with open(LEARNING_FILE, "a") as f:
        f.write(",".join(map(str, features)) + ", suspicious\n")

def write_key(key):
    try:
        with log_lock:
            with open(KEYLOG_FILE, "a") as f:
                f.write(f"{key.char if hasattr(key, 'char')else str(key)}")
    except Exception:
        pass

def start_typing_monitor():
    print("Starting keystroke behaviour analysis...")
    threading.Thread(target=analyze_typing, daemon=True). start()

    with keyboard.Listener(on_press=write_key) as listener:
        listener.join()

