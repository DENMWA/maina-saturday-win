
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Maina Saturday Win", layout="centered")

st.title("🎯 Maina Saturday Win Predictor")
st.markdown("""
This app uses a hybrid predictive formula that cycles between **Hot**, **Cold**, and **Blend** strategies
while dynamically adapting to the most recent hot/cold trends from Saturday Lotto.
""")

# Load predictions
df = pd.read_csv("Maina_Saturday_Win_Predictions.csv")

# Filter option
strategy = st.selectbox("Filter by Strategy", ['All'] + sorted(df['Strategy'].unique()))
if strategy != 'All':
    df = df[df['Strategy'] == strategy]

st.dataframe(df)

# Download option
st.download_button("📥 Download Filtered Predictions", df.to_csv(index=False), file_name="Filtered_Predictions.csv")
