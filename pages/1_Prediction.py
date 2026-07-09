import streamlit as st

from predict import predict_heart_disease
from database import save_prediction

st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="wide"
)

st.title("❤️ Heart Disease Prediction")

st.write("Fill in the patient information.")

st.divider()

col1, col2 = st.columns(2)

with col1:

    age = st.number_input("Age", 20, 100, 45)

    sex = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )

    cp = st.selectbox(
        "Chest Pain Type",
        [0, 1, 2, 3]
    )

    trestbps = st.number_input(
        "Resting Blood Pressure",
        80,
        250,
        120
    )

    chol = st.number_input(
        "Cholesterol",
        100,
        600,
        200
    )

    fbs = st.selectbox(
        "Fasting Blood Sugar >120",
        [0, 1]
    )

with col2:

    restecg = st.selectbox(
        "Rest ECG",
        [0, 1, 2]
    )

    thalach = st.number_input(
        "Maximum Heart Rate",
        60,
        250,
        150
    )

    exang = st.selectbox(
        "Exercise Induced Angina",
        [0, 1]
    )

    oldpeak = st.number_input(
        "Old Peak",
        0.0,
        10.0,
        1.0
    )

    slope = st.selectbox(
        "Slope",
        [0, 1, 2]
    )

    ca = st.selectbox(
        "CA",
        [0, 1, 2, 3, 4]
    )

    thal = st.selectbox(
        "Thal",
        [0, 1, 2, 3]
    )

st.divider()

if st.button("🔍 Predict", use_container_width=True):

    sex_value = 1 if sex == "Male" else 0

    features = [

        age,
        sex_value,
        cp,
        trestbps,
        chol,
        fbs,
        restecg,
        thalach,
        exang,
        oldpeak,
        slope,
        ca,
        thal

    ]

    prediction, probability = predict_heart_disease(features)

    result = "High Risk" if prediction == 1 else "Low Risk"

    patient = {

        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal,
        "prediction": result,
        "probability": float(probability)

    }

    try:
        save_response = save_prediction(patient)
    except Exception as err:
        save_response = {"error": str(err)}

    st.divider()

    if prediction == 1:
        st.error("🔴 High Risk of Heart Disease")
    else:
        st.success("🟢 Low Risk of Heart Disease")

    st.metric(
        "Confidence",
        f"{probability*100:.2f}%"
    )

    if isinstance(save_response, dict) and save_response.get("saved_locally"):
        st.success("Prediction saved locally in models/predictions_local.json.")
        if save_response.get("message"):
            st.info(save_response["message"])
    elif isinstance(save_response, dict) and save_response.get("error"):
        st.warning("Prediction computed, but save failed: " + str(save_response["error"]))
    else:
        st.success("Prediction saved to Supabase successfully!")