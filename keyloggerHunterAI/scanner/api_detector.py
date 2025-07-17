import psutil
from core.logger import log_alert

SUSPICIOUS_MODULES = [
    "user32.dll",
    "keyboard.dll",
    "hook.dll",
    "winhook.dll",
    "input.dll"
]

def scan_api_usage():
    suspicious_apis = ["SetWindowsHookEx", "GetAsyncKeyState", "GetForegroundWindow"]
    results = []
    flagged_processes = {}

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = " ".join(proc.info['cmdline'])
            score = 0
            for api in suspicious_apis:
                if api.lower() in cmdline.lower():
                    score += 1
            if score >= 2:  # only flag if multiple APIs match
                results.append(f"[!] PID {proc.info['pid']} ({proc.info['name']}) uses multiple suspicious APIs.")
        except Exception:
            continue

    return results