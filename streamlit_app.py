
import streamlit as st
import pandas as pd
import numpy as np
from prediction_engine import score_predictions

st.set_page_config(page_title="Maina Saturday Win", layout="centered")
st.title("🎯 Maina Saturday Win: Adaptive Lotto Predictor")
st.markdown("Continuously learning from your inputs. Built to win, one draw at a time.")

uploaded_file = st.file_uploader("Upload your prediction set CSV with 'Main Numbers'", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'Main Numbers' not in df.columns:
        st.error("CSV must contain a 'Main Numbers' column with 6-number lists.")
    else:
        st.success("Prediction file uploaded. Scoring entries...")

        # Score predictions using ML model
        scored_df = score_predictions(df.copy())

        st.subheader("🔮 ML-Scored Predictions")
        st.dataframe(scored_df[['Main Numbers', 'Score']].head(50))

        csv_download = scored_df.to_csv(index=False)
        st.download_button("📥 Download Scored Predictions", csv_download, file_name="Scored_Predictions.csv")
else:
    st.info("Upload a CSV file to get started.")
