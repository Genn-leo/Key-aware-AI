import winreg
from core.logger import log_alert
import time

SUSPICIOUS_NAMES = ["keylog", "logger", "stealer", "spy", "rat", "inject", "hack", "hook", "trojan", "backdoor", "malware", "virus", "worm", "exploit", "payload"]
SUSPICIOUS_PATHS = ["AppData", "Temp", "Roaming", "startup", "System32", "ProgramData", "LocalService", "NetworkService"]

REG_PATHS = [
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\Windows"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon"),
]

def scan_registry():
    print(" Starting registry scan...")

    while True:
        flagged = []

        for hive, path in REG_PATHS:
            try:
                reg_key = winreg.OpenKey(hive, path, 0, winreg.KEY_READ)
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(reg_key, i)
                        for keyword in SUSPICIOUS_NAMES:
                            if keyword in name.lower() or keyword in value.lower():
                                flagged.append((path, name, value))
                        for p in SUSPICIOUS_PATHS:
                            if p.lower() in value.lower():
                                flagged.append((path, name, value))
                        i += 1
                    except OSError:
                        break
            except Exception:
                continue

        if flagged:
            for reg_path, name, value in flagged:
                log_alert(f" Registry persistence flag: {name} -> {value} in {reg_path}")
        else:
            print("Registry scan clean.")

        time.sleep(60)
