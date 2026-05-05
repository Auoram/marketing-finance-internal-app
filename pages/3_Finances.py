import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.title("💰 Financial Consulting Dashboard")

conn = sqlite3.connect('app.db')

# Metrics row
col1, col2, col3, col4 = st.columns(4)
total_invoices = pd.read_sql("SELECT COUNT(*) as cnt FROM invoices", conn).iloc[0]['cnt']
total_revenue = pd.read_sql("SELECT SUM(amount) as total FROM invoices WHERE status='paid'", conn).iloc[0]['total']
pending = pd.read_sql("SELECT COUNT(*) as cnt FROM invoices WHERE status='pending'", conn).iloc[0]['cnt']
avg_hours = pd.read_sql("SELECT AVG(hours_tracked) as avg FROM invoices", conn).iloc[0]['avg']

col1.metric("Total Invoices", total_invoices)
col2.metric("Revenue", f"{total_revenue:,.0f} MAD" if total_revenue else 0)
col3.metric("Pending", pending)
col4.metric("Avg Hours/Client", f"{avg_hours:.1f}" if avg_hours else 0)

# Cash Flow Chart
st.subheader("📊 Cash Flow Forecast")
df_flow = pd.read_sql("""
    SELECT status, SUM(amount) as amount 
    FROM invoices GROUP BY status
""", conn)
fig = px.pie(df_flow, names='status', values='amount', title="Invoice Status Breakdown")
st.plotly_chart(fig, use_container_width=True)

# Billing Form
st.subheader("➕ New Invoice / Time Tracking")
client_df = pd.read_sql("SELECT id, name FROM clients", conn)
client_id = st.selectbox("Client", client_df['name'].tolist(), format_func=lambda x: x)
hours = st.number_input("Hours Tracked", min_value=0.0, value=10.0)
rate = st.number_input("Hourly Rate (MAD)", value=500.0)
amount = hours * rate
st.number_input("Amount", value=amount, disabled=True)
due_date = st.date_input("Due Date", datetime.now() + timedelta(days=30))

if st.button("Generate Invoice"):
    cur = conn.cursor()
    cur.execute("INSERT INTO invoices (client_id, amount, hours_tracked, due_date) VALUES (?, ?, ?, ?)",
                (client_df[client_df['name']==client_id]['id'].iloc[0], amount, hours, due_date))
    conn.commit()
    st.success("Invoice created!")
    st.rerun()

# Invoices Table
st.subheader("All Invoices")
df_invoices = pd.read_sql("""
    SELECT i.*, c.name as client_name 
    FROM invoices i 
    JOIN clients c ON i.client_id = c.id 
    ORDER BY i.id DESC
""", conn)
st.dataframe(df_invoices)

conn.close()