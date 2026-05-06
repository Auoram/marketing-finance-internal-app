import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('app.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            preferences TEXT,
            budget REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            channel TEXT,
            spend REAL,
            roi REAL,
            clicks INTEGER,
            status TEXT DEFAULT 'active',
            FOREIGN KEY(client_id) REFERENCES clients (id)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            amount REAL,
            hours_tracked REAL,
            status TEXT DEFAULT 'pending',
            due_date DATE,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            client_id INTEGER,
            status TEXT DEFAULT 'draft',  -- draft/approved/published
            file_path TEXT,
            scheduled_date DATE,
            version INTEGER DEFAULT 1,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )
    ''')
    conn.commit()
    conn.close()

def get_clients():
    conn = sqlite3.connect('app.db')
    df = pd.read_sql_query("SELECT * FROM clients ORDER BY created_at DESC", conn)
    conn.close()
    return df

def add_client(name, email, preferences, budget):
    conn = sqlite3.connect('app.db')
    conn.execute("INSERT INTO clients (name, email, preferences, budget) VALUES (?, ?, ?, ?)",
                 (name, email, preferences, budget))
    client_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    conn.close()
    return client_id

def add_campaign(client_id, channel, spend, roi):
    conn = sqlite3.connect('app.db')
    conn.execute("INSERT INTO campaigns (client_id, channel, spend, roi) VALUES (?, ?, ?, ?)",
                 (client_id, channel, spend, roi))
    conn.commit()
    conn.close()

def seed_campaigns():
    df = pd.read_csv('data/campaigns.csv')
    conn = sqlite3.connect('app.db')
    df.to_sql('campaigns', conn, if_exists='append', index=False)
    conn.close()
    print('Seeded 100 campaigns!')

if __name__ == "__main__": init_db(); print("DB ready!")