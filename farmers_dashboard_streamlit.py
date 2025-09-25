import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Farmer's Dashboard", layout="wide")

st.title("🌱 Farmer's Dashboard")
st.markdown("Helping farmers decide **What to Plant?** and **When to Sell?** for maximum profit.")

# ------------------------------
# SIDEBAR NAVIGATION
# ------------------------------
page = st.sidebar.radio("Choose a page:", ["🌾 What to Plant?", "💰 When to Sell?"])

# ------------------------------
# PAGE 1: WHAT TO PLANT?
# ------------------------------
if page == "🌾 What to Plant?":
    st.header("🌾 Profit Maximizer: Your Planting Guide")

    # Inputs
    region = st.selectbox("Select your Region/District", ["Nashik, Maharashtra", "Bengaluru, Karnataka"])
    season = st.selectbox("Select Planting Season", ["Kharif", "Rabi", "Summer"])

    # Mock prediction data
    crops = ["Onion", "Potato", "Tomato", "Wheat", "Rice"]
    profits = np.random.randint(10, 50, size=len(crops))  # random profits in ₹/kg

    df = pd.DataFrame({"Crop": crops, "Predicted Profit (₹/kg)": profits})
    fig = px.bar(df, x="Crop", y="Predicted Profit (₹/kg)", color="Predicted Profit (₹/kg)", 
                 color_continuous_scale="Greens", title="Top Crops by Predicted Profit")

    st.plotly_chart(fig, use_container_width=True)

    # Dynamic recommendation
    best_crop = df.loc[df["Predicted Profit (₹/kg)"].idxmax()]
    st.success(f"✅ Based on data for **{season} in {region}**, the most profitable crop is "
               f"**{best_crop['Crop']}** with expected returns of ₹{best_crop['Predicted Profit (₹/kg)']}/kg.")

# ------------------------------
# PAGE 2: WHEN TO SELL?
# ------------------------------
elif page == "💰 When to Sell?":
    st.header("💰 Harvest Planner: When to Sell for Maximum Profit")

    # Inputs
    crop = st.selectbox("Select your Harvested Crop", ["Onion", "Potato", "Tomato", "Wheat", "Rice"])
    storage_weeks = st.slider("Select Storage Duration (weeks)", 0, 12, 0)
    current_price = st.number_input("Enter Current Market Price (₹/kg)", min_value=1, value=20)

    # Mock price forecast (simulate future trend)
    weeks = list(range(13))
    forecast = [current_price + np.sin(i/2) * 5 + np.random.randint(-2, 2) for i in weeks]

    df_forecast = pd.DataFrame({"Week": weeks, "Predicted Price (₹/kg)": forecast})

    fig = px.line(df_forecast, x="Week", y="Predicted Price (₹/kg)",
                  title=f"Price Forecast for {crop} (next 12 weeks)", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Recommendation logic
    future_price = df_forecast.loc[df_forecast["Week"] == storage_weeks, "Predicted Price (₹/kg)"].values[0]
    if future_price > current_price:
        st.info(f"📈 Current price: ₹{current_price}/kg. If you store for {storage_weeks} weeks, "
                f"expected price = ₹{future_price:.2f}/kg. **Recommendation: Store your crop.**")
    else:
        st.warning(f"📉 Current price: ₹{current_price}/kg. Price may drop to ₹{future_price:.2f}/kg "
                   f"in {storage_weeks} weeks. **Recommendation: Sell now.**")
