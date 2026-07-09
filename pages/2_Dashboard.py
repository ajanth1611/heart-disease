from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "heart_clean.csv"


st.set_page_config(page_title="Dashboard", page_icon="chart")

st.title("Heart Disease Dashboard")

df = pd.read_csv(DATA_PATH)

total_patients = len(df)
disease = len(df[df["target"] == 1])
healthy = len(df[df["target"] == 0])

col1, col2, col3 = st.columns(3)

col1.metric("Total Patients", total_patients)
col2.metric("Heart Disease", disease)
col3.metric("Healthy", healthy)

st.markdown("---")

fig = px.pie(
    df,
    names="target",
    title="Heart Disease Distribution",
    hole=0.45,
)
st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(
    df,
    x="age",
    nbins=20,
    title="Age Distribution",
)
st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(
    df,
    x="chol",
    nbins=20,
    title="Cholesterol Distribution",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Correlation Matrix")

numeric_df = df.select_dtypes(include=["number"])
corr = numeric_df.corr()

st.dataframe(corr.round(2))
