import joblib

model = joblib.load("ml/keylogger_model.joblib")
sample = [[0.07, 0.82, 200, 12]]
result = model.predict(sample)

print("Suspicious" if result[0] == 1 else "Normal")