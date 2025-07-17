import os
import csv
from core.behavior_analyzer import extract_features as extract_typing_features
from scanner.process_scanner import is_suspicious_process
from scanner.api_detector import SUSPICIOUS_MODULES
from scanner.registry_scanner import REG_PATHS, SUSPICIOUS_NAMES
from scanner.file_checker import WATCH_DIRS, SUSPICIOUS_KEYWORDS, SUSPICIOUS_EXTENSIONS
import psutil
import winreg
from datetime import datetime, timedelta

FEATURE_PATH = "data/features_full.csv"
KEYLOG_FILE = "data/temp_log.txt"

# Make sure path exists
os.makedirs("data", exist_ok=True)

# Initialize file with headers if not exists
if not os.path.exists(FEATURE_PATH):
    with open(FEATURE_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "avg_delay", "burst_ratio", "total_keys", "unique_keys",
            "suspicious_proc_count", "total_processes", "unsigned_processes", "fake_svchost_count",
            "suspicious_api_modules", "total_loaded_modules",
            "suspicious_files", "recent_executables", "suspicious_file_paths",
            "suspicious_registry_keys", "registry_total_checked",
            "label"
        ])

def get_process_features():
    suspicious = 0
    unsigned = 0
    fake_svchost = 0
    total = 0

    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        total += 1
        try:
            flag, name, path = is_suspicious_process(proc)
            if flag:
                suspicious += 1
            if name and "svchost" in name.lower() and "svch0st" in name.lower():
                fake_svchost += 1
            if not proc.exe() or not os.path.exists(proc.exe()):
                unsigned += 1
        except:
            continue
    return suspicious, total, unsigned, fake_svchost

def get_api_features():
    suspicious_count = 0
    module_total = 0

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            mem_maps = proc.memory_maps()
            module_total += len(mem_maps)
            for m in mem_maps:
                for keyword in SUSPICIOUS_MODULES:
                    if keyword in m.path.lower():
                        suspicious_count += 1
        except:
            continue
    return suspicious_count, module_total

def get_file_features():
    recent_exes = 0
    suspicious_files = 0
    suspicious_paths = 0
    now = datetime.now()

    for folder in WATCH_DIRS:
        if not os.path.exists(folder):
            continue
        for root, _, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                try:
                    ext = os.path.splitext(file)[1].lower()
                    created = datetime.fromtimestamp(os.path.getctime(path))
                    # Only flag if BOTH extension and keyword match, AND file is in a suspicious path
                    if (
                        ext in SUSPICIOUS_EXTENSIONS and
                        any(k in file.lower() for k in SUSPICIOUS_KEYWORDS) and
                        any(p in path.lower() for p in ["appdata", "temp", "roaming"])
                    ):
                        suspicious_files += 1
                        suspicious_paths += 1
                        if (now - created) < timedelta(minutes=30):
                            recent_exes += 1
                except Exception:
                    continue
    return suspicious_files, recent_exes, suspicious_paths

def get_registry_features():
    suspicious = 0
    total = 0

    for hive, path in REG_PATHS:
        try:
            reg_key = winreg.OpenKey(hive, path, 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(reg_key, i)
                    total += 1
                    if any(k in name.lower() or k in value.lower() for k in SUSPICIOUS_NAMES):
                        suspicious += 1
                    i += 1
                except OSError:
                    break
        except:
            continue
    return suspicious, total

def main():
    print(" Building full feature vector...")

    typing = extract_typing_features(KEYLOG_FILE) or [0, 0, 0, 0]
    proc = get_process_features()
    apis = get_api_features()
    files = get_file_features()
    reg = get_registry_features()

    # Ask user to label
    print("\n Is this sample normal (0) or suspicious (1)?")
    label = input("Label (0/1): ").strip()
    label = int(label) if label in ['0', '1'] else 0

    features = typing + list(proc) + list(apis) + list(files) + list(reg) + [label]

    with open(FEATURE_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(features)

    print(" Sample added to features_full.csv")

if __name__ == "__main__":
    main()
