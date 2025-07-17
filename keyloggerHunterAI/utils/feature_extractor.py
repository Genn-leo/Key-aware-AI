import os
import pandas as pd

def extract_features_from_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    # Basic typing behavior features
    total_keys = len(lines)
    backspaces = sum(1 for line in lines if 'Backspace' in line)
    enters = sum(1 for line in lines if 'Enter' in line)
    shifts = sum(1 for line in lines if 'Shift' in line)
    specials = sum(1 for line in lines if len(line.strip()) > 1 and not line.strip().isalnum())
    avg_key_length = sum(len(line.strip()) for line in lines) / total_keys if total_keys > 0 else 0

    return {
        "total_keys": total_keys,
        "backspaces": backspaces,
        "enters": enters,
        "shifts": shifts,
        "special_keys": specials,
        "avg_key_length": avg_key_length,
    }

def generate_dataset(folder_path, label):
    rows = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not file_path.endswith(".txt"):
            continue
        try:
            features = extract_features_from_file(file_path)
            features["label"] = label
            rows.append(features)
        except Exception as e:
            print(f" Failed to read {file_path}: {e}")
            continue

    return pd.DataFrame(rows)
