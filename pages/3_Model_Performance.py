from pathlib import Path
import json

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_CSV_PATH = PROJECT_ROOT / "data" / "processed" / "heart_clean.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "xgboost_model.pkl"
METRICS_PATH = PROJECT_ROOT / "models" / "metrics.json"


st.set_page_config(
    page_title="Model Performance",
    page_icon="chart",
    layout="wide",
)

st.title("XGBoost Model Performance")

if not METRICS_PATH.exists():
    st.error("Metrics file not found. Run models/train_model.py first.")
    st.stop()

with open(METRICS_PATH, "r") as f:
    metrics = json.load(f)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Train Accuracy", f"{metrics['Training Accuracy'] * 100:.2f}%")
col2.metric("Test Accuracy", f"{metrics['Testing Accuracy'] * 100:.2f}%")
col3.metric("Precision", f"{metrics['Precision'] * 100:.2f}%")
col4.metric("Recall", f"{metrics['Recall'] * 100:.2f}%")
col5.metric("F1 Score", f"{metrics['F1 Score'] * 100:.2f}%")

st.markdown("---")

model = joblib.load(MODEL_PATH)
df = pd.read_csv(CLEAN_CSV_PATH)

features = df.drop("target", axis=1).columns
importance = model.feature_importances_

feature_df = pd.DataFrame(
    {
        "Feature": features,
        "Importance": importance,
    }
).sort_values(by="Importance", ascending=True)

fig = px.bar(
    feature_df,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Feature Importance (XGBoost)",
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(
    feature_df.sort_values(by="Importance", ascending=False)
)
