import tkinter as tk
from tkinter import messagebox
import joblib
import os

# Load trainer model
MODEL_PATH = os.path.join("..", "ml", "keylogger_model.joblib")
model = joblib.load(MODEL_PATH)

# Prediction function
def predict_behaviour():
    try:
        # get input values
        avg_delay = float(entry_avg_delay.get())
        burst_ratio = float(entry_burst_ratio.get())
        total_keys = int(entry_total_keys.get())
        unique_keys = int(entry_unique_keys.get())

        # Create input for model
        features = [[avg_delay, burst_ratio, total_keys, unique_keys]]
        prediction = model.predict(features)[0]

        # Show result
        result = "Suspicious" if prediction == 1 else "Normal"
        messagebox.showinfo("Prediction Result", f"Result: {result}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Create GUI
root = tk.Tk()
root.title("AI Keylogger Behaviour Detector")

tk.Label(root, text="Average Delay (e.g. 0.05):").grid(row=0, column=0, sticky="w")
entry_avg_delay = tk.Entry(root)
entry_avg_delay.grid(row=0, column=1)

tk.Label(root, text="Burst Ratio (e.g. 0.75):").grid(row=1, column=0, sticky="w")
entry_burst_ratio = tk.Entry(root)
entry_burst_ratio.grid(row=1, column=1)

tk.Label(root, text="Total Keys (e.g. 200):").grid(row=2, column=0, sticky="w")
entry_total_keys = tk.Entry(root)
entry_total_keys.grid(row=2, column=1)

tk.Label(root, text="Unique Keys (e.g. 12):").grid(row=3, column=0, sticky="w")
entry_unique_keys = tk.Entry(root)
entry_unique_keys.grid(row=3, column=1)

tk.Button(root, text="Predict", command=predict_behaviour).grid(row=4, columnspan=2)

root.mainloop()