import os
import pandas as pd

def extract_features(log_file):
    with open(log_file, "r") as f:
        lines = f.readlines()

    times = []
    keys = []

    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            keys.append(parts[0])
            times.append(float(parts[1]))

    if len(times) < 2:
        return None

    delays = [times[i+1] - times[i] for i in range(len(times)-1)]
    burst_ratio = sum(1 for d in delays if d < 0.1) / len(delays)

    return {
        "avg_delay": sum(delays)/len(delays),
        "burst_ratio": burst_ratio,
        "total_keys": len(keys),
        "unique_keys": len(set(keys))
    }

def generate_dataset(folder_path, label):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            features = extract_features(os.path.join(folder_path, filename))
            if features:
                features["label"] = label
                data.append(features)
    return data
