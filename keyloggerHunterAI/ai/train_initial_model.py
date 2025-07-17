import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

DATA_PATH = "data/features_full.csv"
MODEL_PATH = "ai/behavior_model.joblib"

def train_initial_model():
    print(" Training initial AI model with FULL behavior & system features...")

    if not os.path.exists(DATA_PATH):
        print(" features_full.csv not found!")
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

        print(f" Model trained with accuracy: {acc:.2f}")
        print(classification_report(y_test, y_pred))

        joblib.dump(model, MODEL_PATH)
        print(f" New model saved to {MODEL_PATH}")

    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    train_initial_model()
