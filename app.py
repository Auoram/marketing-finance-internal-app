import streamlit as st
import pandas as pd
from src.db import init_db, get_clients, add_client

st.set_page_config(layout="wide", page_title="Marketing Finance App")
init_db()

tab1, tab2 = st.tabs(["📊 Clients", "➕ Add Client"])

with tab1:
    st.subheader("Client Database")
    df = get_clients()
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("New Client")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        email = st.text_input("Email")
    with col2:
        preferences = st.text_area("Preferences (e.g., 'prefers Facebook Ads')")
        budget = st.number_input("Monthly Budget (MAD)", min_value=0.0, value=5000.0)
    if st.button("Save Client", type="primary"):
        if name:
            add_client(name, email, preferences, budget)
            st.success("✅ Client added!")
            st.rerun()
        else:
            st.error("Name required")