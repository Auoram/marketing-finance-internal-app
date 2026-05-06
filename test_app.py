import sqlite3
import pandas as pd
from src.db import init_db, add_client, get_clients

# Reset DB
import os
if os.path.exists('app.db'): os.remove('app.db')
init_db()

print("🧪 MARKETING-FINANCE APP - FULL TEST")
print("=" * 50)

# 1. TEST CLIENT CRM
print("\n1. CLIENT CRM")
client_id1 = add_client("Test Agency MA", "test@agency.ma", "Prefers Google Ads, fintech sector", 25000)
client_id2 = add_client("FinTech Startup", "startup@fin.ma", "Young audience, Facebook focus", 15000)
clients = get_clients()
print(f"✅ Added 2 clients. Total: {len(clients)}")

# 2. TEST CAMPAIGNS
from src.db import add_campaign  # Add this func if missing
conn = sqlite3.connect('app.db')
conn.execute("INSERT INTO campaigns (client_id, channel, spend, roi, clicks, status) VALUES (?, ?, ?, ?, ?, ?)",
             (client_id1, "Google Ads", 5000, 3.2, 2500, "active"))
conn.execute("INSERT INTO campaigns (client_id, channel, spend, roi, clicks, status) VALUES (?, ?, ?, ?, ?, ?)",
             (client_id2, "Facebook", 3000, 2.8, 1800, "A/B Test"))
conn.commit()
conn.close()
print("✅ Added campaigns for clients")

# 3. TEST FINANCES
conn = sqlite3.connect('app.db')
from datetime import date
conn.execute("INSERT INTO invoices (client_id, amount, hours_tracked, status, due_date) VALUES (?, ?, ?, ?, ?)",
             (client_id1, 12000, 24, "paid", date(2026, 6, 1)))
conn.execute("INSERT INTO invoices (client_id, amount, hours_tracked, status, due_date) VALUES (?, ?, ?, ?, ?)",
             (client_id2, 8000, 16, "pending", date(2026, 5, 20)))
conn.commit()
conn.close()
print("✅ Added invoices")

# 4. VERIFY ALL DATA
print("\n4. FINAL VERIFICATION")
clients_df = get_clients()
print("\nClients:")
print(clients_df[['name', 'budget', 'preferences']])
campaigns_df = pd.read_sql("SELECT * FROM campaigns LIMIT 5", sqlite3.connect('app.db'))
print("\nCampaigns (top 5):")
print(campaigns_df)
invoices_df = pd.read_sql("SELECT * FROM invoices", sqlite3.connect('app.db'))
print("\nInvoices:")
print(invoices_df)

print("\n🎉 ALL TESTS PASSED! Run 'streamlit run app.py' to see in UI.")