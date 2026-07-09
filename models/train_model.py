from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier # type: ignore


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_CSV_PATH = PROJECT_ROOT / "data" / "processed" / "heart_clean.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "xgboost_model.pkl"
SCALER_PATH = PROJECT_ROOT / "models" / "scaler.pkl"
METRICS_PATH = PROJECT_ROOT / "models" / "metrics.json"


df = pd.read_csv(CLEAN_CSV_PATH)

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    random_state=42,
    eval_metric="logloss",
    use_label_encoder=False,
)

model.fit(X_train_scaled, y_train)
train_pred = model.predict(X_train_scaled)
y_pred = model.predict(X_test_scaled)
train_accuracy = accuracy_score(y_train, train_pred)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("=" * 50)
print("XGBOOST RESULTS")
print("=" * 50)
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print("\nClassification Report")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred))

joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

metrics = {
    "Training Accuracy": train_accuracy,
    "Testing Accuracy": accuracy,
    "Precision": precision,
    "Recall": recall,
    "F1 Score": f1,
}

with open(METRICS_PATH, "w") as f:
    json.dump(metrics, f, indent=4)

print("\nModel saved successfully!")
