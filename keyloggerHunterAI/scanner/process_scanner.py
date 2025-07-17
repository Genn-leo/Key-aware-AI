import os
import time
import psutil
from core.logger import log_alert

# Keywords we flag as suspicious
SUSPICIOUS_KEYWORDS = ["keylog", "logger", "stealer", "grabber", "sniffer", "inject", "hook", "spy", "logkey", "monitor", "trojan", "rat", "backdoor", "malware", "virus", "worm", "exploit", "payload",
                       "keylog.exe", "logger.exe","inject.exe","rat.exe","stealer.exe","spy.exe","sniffer.exe","grabber.exe","hook.exe", "trojan.exe","backdoor.exe","malware.exe", "virus.exe","worm.exe","exploit.exe", "payload.exe",
                           ".dll", ".bat", ".cmd"]
SUSPICIOUS_LOCATIONS = ["AppData", "Temp", "Roaming", "System32", "ProgramData", "LocalService", "NetworkService", "Windows", "Program Files", "Common Files", "Startup"]

def is_suspicious_process(proc):
    try:
        name = proc.name().lower()
        exe = proc.exe()
        suspicious = False

        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword in name or keyword in exe.lower():
                suspicious = True

        for folder in SUSPICIOUS_LOCATIONS:
            if folder.lower() in exe.lower():
                suspicious = True

        if name.count("svchost") > 1 or "svch0st" in name:
            suspicious = True

        return suspicious, name, exe

    except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess):
        return False, None, None

def scan_processes():
    while True:
        flagged = []

        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            suspicious, name, exe = is_suspicious_process(proc)

            if suspicious and name and exe:
                flagged.append((name, exe))

        if flagged:
            for name, exe in flagged:
                log_alert(f" Suspicious process detected: {name} ({exe})")

        else:
            print(" Process scan clean.")

        time.sleep(30)  # Scan every 30 seconds
