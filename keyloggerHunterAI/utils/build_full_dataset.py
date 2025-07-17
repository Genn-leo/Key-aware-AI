import os
import pandas as pd
from utils.feature_extractor import generate_dataset

if __name__ == "__main__":
    print(" Building full dataset...")

    normal = generate_dataset("data/keylogs/normal", label=0)
    malware = generate_dataset("data/keylogs/malicious", label=1)

    full_data = pd.concat([normal, malware], ignore_index=True)
    full_data.to_csv("data/features_full.csv", index=False)

    print(" Dataset saved to data/features_full.csv")
