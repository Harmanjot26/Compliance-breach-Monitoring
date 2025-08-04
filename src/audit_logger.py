import sqlite3

def setup_db(db_path='audit.db'):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS breaches (
            transaction_id INTEGER,
            client_id TEXT,
            timestamp TEXT,
            breach_types TEXT
        )
    """)
    return conn

def log_breaches(conn, breaches_df):
    breaches_df.to_sql('breaches', conn, if_exists='append', index=False)
    conn.commit()
