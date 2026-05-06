import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title("📊 Analytics Dashboard - ROI & Heatmaps")

conn = sqlite3.connect('app.db')

# ROI Metrics
df_camp = pd.read_sql("SELECT * FROM campaigns", conn)
if not df_camp.empty:
    fig_roi = px.bar(df_camp, x='channel', y='roi', color='client_id', title="ROI by Channel")
    st.plotly_chart(fig_roi)

    # Heatmap: Spend vs ROI
    fig_heat = px.density_heatmap(df_camp, x='spend', y='roi', title="Spend vs ROI Heatmap",
                                  nbinsx=20, nbinsy=20, color_continuous_scale="Viridis")
    st.plotly_chart(fig_heat)

    # Conversion Mock (clicks proxy)
    st.metric("Total Clicks", df_camp['clicks'].sum())
    st.metric("Avg Conversion", (df_camp['clicks'] / df_camp['spend'] * 1000).mean().round(2))

conn.close()