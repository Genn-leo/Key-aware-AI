from feature_extractor import generate_dataset
import pandas as pd

normal_data = generate_dataset("data/keylogs/normal/", label=0)
malicious_data = generate_dataset("data/keylogs/malicious", label=1)

df = pd.DataFrame(normal_data + malicious_data)
df.to_csv("data/features.csv", index=False)
print("Dataset saved to data/features.csv")
