import sys
from pathlib import Path
import joblib
import numpy as np

if sys.version_info < (3, 7):
    raise RuntimeError(
        "This app requires Python 3.7 or newer. "
        "Run it with the bundled environment: .\\venv37\\Scripts\\python.exe -m streamlit run pages\\1_Prediction.py"
    )

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "xgboost_model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


def predict_heart_disease(features):
    features = np.array(features).reshape(1, -1)
    scaled = scaler.transform(features)
    prediction = model.predict(scaled)[0]
    probability = model.predict_proba(scaled)[0][prediction]
    return prediction, probability