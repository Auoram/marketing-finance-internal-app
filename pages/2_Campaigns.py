import streamlit as st
import pandas as pd
import sqlite3
from src.db import seed_campaigns  # Remove after first run

st.title("📈 Campaign Management")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("All Campaigns")
    conn = sqlite3.connect('app.db')
    df = pd.read_sql_query("""
        SELECT c.*, cl.name as client_name 
        FROM campaigns c 
        JOIN clients cl ON c.client_id = cl.id 
        ORDER BY c.id DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("Quick Stats")
    total_spend = df['spend'].sum()
    st.metric("Total Spend", round(total_spend, 0) if total_spend else 0)
    avg_roi = df['roi'].mean()
    st.metric("Avg ROI", round(avg_roi, 2) if not pd.isna(avg_roi) else 0)
    if st.button("🔄 Refresh Data"):
        st.rerun()

# New Campaign Form
st.subheader("➕ New Campaign / A/B Test")
with st.form("new_campaign"):
    client_id = st.selectbox("Client", pd.read_sql("SELECT id, name FROM clients", sqlite3.connect('app.db'))['name'].tolist())
    channel = st.selectbox("Channel", ['Google Ads', 'Facebook', 'Instagram', 'Email', 'SMS'])
    spend = st.number_input("Spend (MAD)", min_value=0.0)
    expected_roi = st.number_input("Expected ROI", value=2.5)
    notes = st.text_area("A/B Variant or Notes")
    if st.form_submit_button("Launch Campaign"):
        conn = sqlite3.connect('app.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO campaigns (client_id, channel, spend, roi, status) VALUES (?, ?, ?, ?, ?)",
                    (client_id, channel, spend, expected_roi, notes[:50]))
        conn.commit()
        conn.close()
        st.success("Campaign launched!")
        st.rerun()