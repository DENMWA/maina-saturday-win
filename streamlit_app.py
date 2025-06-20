
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Maina Saturday Win", layout="centered")
st.title("📈 Maina Saturday Win: Adaptive Lotto Predictor")

st.markdown("""
Upload your latest **Saturday Lotto draw history CSV** (draw number + 6 main + 2 supplementary),
and get fresh predictions using the hybrid Hot/Cold/Blend strategy informed by recent trends.
""")

# Upload section
uploaded_file = st.file_uploader("Upload your historical Saturday Lotto results", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Clean draw columns
    main_cols = ['Main 1', 'Main 2', 'Main 3', 'Main 4', 'Main 5', 'Main 6']
    supp_cols = ['Supp 1', 'Supp 2']
    draw_cols = main_cols + supp_cols

    # Melt and count frequencies
    all_nums = df[main_cols + supp_cols].apply(pd.to_numeric, errors='coerce')
    freq = all_nums.stack().value_counts().sort_index()

    # Define hot and cold
    hot_list = freq.sort_values(ascending=False).head(10).index.tolist()
    cold_list = freq.sort_values(ascending=True).head(10).index.tolist()

    # Calculate recent hot/cold ratio
    recent_draws = df.sort_values(by='Draw Number', ascending=False).head(10)
    hot_counts = []
    cold_counts = []

    for _, row in recent_draws.iterrows():
        main_numbers = [row[c] for c in main_cols]
        hot_counts.append(sum(n in hot_list for n in main_numbers))
        cold_counts.append(sum(n in cold_list for n in main_numbers))

    expected_hot = round(np.mean(hot_counts))
    expected_hot = max(1, min(expected_hot, 5))  # Clamp between 1 and 5

    st.success(f"Based on your last 10 draws, expected hot count is approximately: {expected_hot}/6")

    # Generate predictions
    strategies = ['hot', 'cold', 'blend']
    all_numbers = list(range(1, 46))
    predictions = []

    for i in range(50):
        strategy = strategies[i % 3]
        valid = False

        # Target hot/cold counts
        if strategy == 'hot':
            hot_target = min(expected_hot + 1, 5)
            cold_target = max(0, 6 - hot_target - 1)
        elif strategy == 'cold':
            hot_target = max(0, expected_hot - 1)
            cold_target = max(2, 6 - hot_target - 1)
        else:  # blend
            hot_target = expected_hot
            cold_target = 6 - hot_target - 2

        while not valid:
            nums = sorted(np.random.choice(all_numbers, 8, replace=False))
            mains = nums[:6]
            supps = nums[6:]
            hot_count = sum(n in hot_list for n in mains)
            cold_count = sum(n in cold_list for n in mains)

            if hot_count >= hot_target and cold_count >= cold_target:
                predictions.append({
                    'Strategy': strategy.capitalize(),
                    'Main Numbers': mains,
                    'Supp Numbers': supps,
                    'Hot Count': hot_count,
                    'Cold Count': cold_count
                })
                valid = True

    result_df = pd.DataFrame(predictions)
    st.subheader("🔮 Fresh Prediction Sets")
    st.dataframe(result_df)

    csv_download = result_df.to_csv(index=False)
    st.download_button("📥 Download Predictions", csv_download, file_name="Predictions.csv")
