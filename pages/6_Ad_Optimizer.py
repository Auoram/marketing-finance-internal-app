import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from src.models import AdOptimizer
from src.db import get_clients

st.title("🤖 AI Ad Optimizer - Stop Ad Losses")

# Load & Train
@st.cache_data
def load_data():
    conn = sqlite3.connect('app.db')
    df = pd.read_sql("SELECT * FROM campaigns WHERE spend > 0", conn)
    conn.close()
    return df

df_ads = load_data()
optimizer = AdOptimizer()
if not df_ads.empty:
    optimizer.train(df_ads)

tab1, tab2, tab3 = st.tabs(["🔍 Detect Losses", "🔮 Predict ROI", "💰 Optimize Budget"])

with tab1:
    st.subheader("Underperforming Ads")
    underperform = optimizer.detect_underperform(df_ads)
    if not underperform.empty:
        st.warning(f"🚨 Found {len(underperform)} wasteful campaigns - reallocate now!")
        st.dataframe(underperform)
    else:
        st.success("✅ All good!")

with tab2:
    st.subheader("Predict Campaign ROI")
    spend = st.slider("Spend (MAD)", 100, 10000, 2000)
    clicks = st.slider("Expected Clicks", 50, 5000, 500)
    channel = st.selectbox("Channel", df_ads['channel'].unique())
    if st.button("Predict ROI"):
        roi_pred = optimizer.predict_roi(spend, clicks, channel)
        st.metric("Predicted ROI", f"{roi_pred:.2f}x")
        st.info(f"Suggested: {spend * roi_pred:.0f} MAD revenue")

with tab3:
    st.subheader("Smart Budget Reallocation")
    total_budget = st.number_input("Total Budget (MAD)", 10000, 100000, 50000)
    if st.button("Optimize Allocation"):
        alloc = optimizer.optimize_budget(total_budget)
        st.json(alloc)
        waste_saved = sum(alloc.values()) * 0.2  # Mock 20% savings
        st.balloons()
        st.success(f"💸 Potential savings: {waste_saved:,.0f} MAD (20% efficiency gain)")

# Audience Segmentation Mock
st.subheader("👥 Audience Clusters (K-Means)")
if not df_ads.empty and len(df_ads) >= 3:
    optimizer.kmeans.fit(df_ads[['spend', 'clicks']])
    df_ads_copy = df_ads.copy()
    df_ads_copy['cluster'] = optimizer.kmeans.labels_
    fig = px.scatter(df_ads_copy, x='spend', y='clicks', color='cluster', title="Segment & Target")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("ℹ️ Add 3+ campaigns for clustering")