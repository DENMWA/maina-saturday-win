import streamlit as st
from prediction_engine import generate_predictions, score_predictions, update_historical_and_retrain
from train_model import train_model
import pandas as pd

train_model()  # Ensure model is trained with current environment

st.title("Maina Saturday Win")
st.subheader("♻️ Self-Updating Lotto Predictor")

strategy = st.selectbox("Select Prediction Strategy", ["hot", "cold", "blend"])
if st.button("Generate Predictions"):
    raw_preds = generate_predictions(strategy=strategy)
    scored = score_predictions(raw_preds)
    df = pd.DataFrame([{
        **{f"N{i+1}": num for i, num in enumerate(p["Main"] + p["Supp"])},
        "Score": p["Score"]
    } for p in scored])
    st.dataframe(df)

st.markdown("---")
st.subheader("📥 Upload New Winning Entry")
uploaded = st.file_uploader("Upload a single-row CSV with 8 numbers and Win column", type="csv")
if uploaded:
    new_draw = pd.read_csv(uploaded)
    if new_draw.shape[1] == 9:
        update_historical_and_retrain(new_draw.iloc[0].tolist())
        st.success("Historical data updated and model retrained.")
    else:
        st.error("Please ensure your CSV has 8 number columns + 1 Win label.")