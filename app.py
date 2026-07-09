import streamlit as st


st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="heart",
    layout="wide",
)

st.title("Heart Disease Prediction System")

st.markdown("---")

st.subheader("Project Overview")

st.write(
    """
This application predicts whether a patient is at risk of heart disease
using a machine learning model based on XGBoost.

The model was trained on the Heart Disease Dataset and uses
13 medical features for prediction.
"""
)

st.markdown("---")

st.subheader("Model Information")

col1, col2 = st.columns(2)

with col1:
    st.metric("Algorithm", "XGBoost")
    st.metric("Features", "13")

with col2:
    st.metric("Model Status", "Ready")
    st.metric("Prediction", "Binary")

st.markdown("---")

st.success("Model loaded successfully")
st.info("Open the prediction page to enter patient data and receive a prediction.")
