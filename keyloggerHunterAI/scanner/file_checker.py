import os
import time
from core.logger import log_alert
from datetime import datetime, timedelta
from pathlib import Path

SUSPICIOUS_KEYWORDS = ["keylog", "logger", "inject", "rat", "stealer", "spy", "sniffer", "grabber", "hook", "trojan", "backdoor", "malware", "virus", "worm", "exploit", "payload"]
SUSPICIOUS_EXTENSIONS = ["keylog.exe", "logger.exe","inject.exe","rat.exe","stealer.exe","spy.exe","sniffer.exe","grabber.exe","hook.exe", "trojan.exe","backdoor.exe","malware.exe", "virus.exe","worm.exe","exploit.exe", "payload.exe"
                         ".bat", ".dll", ".cmd"]

# Dynamically get current user's folders
user_home = str(Path.home())
WATCH_DIRS = [
    os.path.join(user_home, "AppData", "Roaming"),
    os.path.join(user_home, "AppData", "Local", "Temp"),
    os.path.join(user_home, "Downloads"),
    "C:\\ProgramData"
]

def scan_files():
    print(" Starting file system scan...")

    while True:
        flagged = []
        now = datetime.now()

        for folder in WATCH_DIRS:
            if not os.path.exists(folder):
                continue

            for root, _, files in os.walk(folder):
                for file in files:
                    path = os.path.join(root, file)
                    try:
                        ext = os.path.splitext(file)[1].lower()
                        stat = os.stat(path)
                        created = datetime.fromtimestamp(stat.st_ctime)
                        modified = datetime.fromtimestamp(stat.st_mtime)

                        suspicious_name = any(k in file.lower() for k in SUSPICIOUS_KEYWORDS)
                        suspicious_ext = ext in SUSPICIOUS_EXTENSIONS
                        recent = (now - created) < timedelta(minutes=30)

                        if suspicious_ext and (suspicious_name or recent):
                            flagged.append(path)

                    except Exception:
                        continue

        if flagged:
            for f in flagged:
                log_alert(f" Suspicious file detected: {f}")
        else:
            print(" File scan clean.")

        time.sleep(90)
