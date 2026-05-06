import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.title("📅 Content Calendar & Asset Library")

# Simple calendar (dates + status)
conn = sqlite3.connect('app.db')
df_content = pd.read_sql("""
    SELECT c.*, cl.name as client_name 
    FROM content c LEFT JOIN clients cl ON c.client_id = cl.id
""", conn)

st.subheader("Content Overview")
st.dataframe(df_content, use_container_width=True)

# Add Content
st.subheader("➕ New Content / Asset")
client_df = pd.read_sql("SELECT id, name FROM clients", conn)
col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Title")
    client_id = st.selectbox("Client", client_df['name'].tolist())
    file_path = st.file_uploader("Upload Asset").name if st.file_uploader("Upload Asset") else "no-file"
with col2:
    status = st.selectbox("Status", ["draft", "review", "approved", "published"])
    scheduled = st.date_input("Schedule Date")
    version = st.number_input("Version", value=1)

if st.button("Save Content"):
    cur = conn.cursor()
    cur.execute("INSERT INTO content (title, client_id, status, file_path, scheduled_date, version) VALUES (?, ?, ?, ?, ?, ?)",
                (title, client_df[client_df['name']==client_id]['id'].iloc[0], status, file_path, scheduled, version))
    conn.commit()
    st.success("Content scheduled!")
    st.rerun()

# Workflow Automation Mock
st.subheader("⚙️ Automated Workflows")
workflow = st.selectbox("Trigger", ["Send Email Nurture", "SMS Reminder", "Lead Alert"])
if st.button("Run Workflow"):
    st.success(f"✅ Mock {workflow} sent to {len(df_content)} items!")
    st.balloons()

conn.close()