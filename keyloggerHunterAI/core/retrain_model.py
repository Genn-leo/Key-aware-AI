import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import shutil

DATA_PATH = "data/features_full.csv"
MODEL_PATH = "ai/behavior_model.joblib"
BACKUP_PATH = "ai/behavior_model.old.joblib"

def retrain_model():
    print(" Retraining AI model with combined full-system behavior...")

    if not os.path.exists(DATA_PATH):
        print(" features_full.csv not found.")
        return

    try:
        df = pd.read_csv(DATA_PATH)

        if df.empty or "label" not in df.columns:
            print(" Dataset is empty or malformed.")
            return

        X = df.drop("label", axis=1)
        y = df["label"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        print(f" Retrained model accuracy: {acc:.2f}")
        print(classification_report(y_test, y_pred))

        if os.path.exists(MODEL_PATH):
            shutil.copy2(MODEL_PATH, BACKUP_PATH)

        joblib.dump(model, MODEL_PATH)
        print(" Updated model saved.")

    except Exception as e:
        print(f" Error retraining model: {e}")

if __name__ == "__main__":
    retrain_model()
