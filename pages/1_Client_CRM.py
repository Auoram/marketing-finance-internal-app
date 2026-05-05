import streamlit as st
import sqlite3
import pandas as pd

st.title("👥 Client CRM")

# Sidebar filters
st.sidebar.header("Filters")
client_name = st.sidebar.text_input("Search Name")

# Load data
conn = sqlite3.connect('app.db')
df = pd.read_sql_query("""
    SELECT * FROM clients 
    ORDER BY created_at DESC
""", conn)

if client_name:
    df = df[df['name'].str.contains(client_name, case=False, na=False)]

st.subheader("All Clients")
st.dataframe(df, use_container_width=True)

# Client details expander
for idx, row in df.iterrows():
    with st.expander(f"📋 {row['name']} (Budget: {row['budget']})"):
        st.write(f"**Email**: {row['email']}")
        st.write(f"**Preferences**: {row['preferences']}")
        st.info(f"ID: {row['id']} | Created: {row['created_at']}")

# Edit/Delete
st.subheader("Actions")
selected_id = st.selectbox("Select Client to Edit/Delete", df['id'].tolist() if not df.empty else [0])
if selected_id and selected_id != 0:
    cur = conn.cursor()
    client = pd.read_sql(f"SELECT * FROM clients WHERE id={selected_id}", conn).iloc[0]
    
    new_name = st.text_input("New Name", client['name'])
    new_budget = st.number_input("New Budget", value=float(client['budget']))
    
    col1, col2 = st.columns(2)
    if col1.button("Update"):
        cur.execute("UPDATE clients SET name=?, budget=? WHERE id=?", (new_name, new_budget, selected_id))
        conn.commit()
        st.success("Updated!")
        st.rerun()
    if col2.button("Delete", type="secondary"):
        cur.execute("DELETE FROM clients WHERE id=?", (selected_id,))
        conn.commit()
        st.warning("Deleted!")
        st.rerun()

conn.close()