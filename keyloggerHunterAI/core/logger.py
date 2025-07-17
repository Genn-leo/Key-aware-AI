import os
import time

LOG_FILE = "reports/alerts.log"

# Make sure directory exists
os.makedirs("reports", exist_ok=True)

def log_alert(message):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}"
    print(full_message)

    with open(LOG_FILE, "a") as f:
        f.write(full_message + "\n")
