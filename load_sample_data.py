"""
Loads sample_data.csv into the SQLite database.
Run this after `python MRD_LR/manage.py migrate` to get the app working immediately.

Usage:
    python load_sample_data.py
"""
import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("MRD_LR", "db.sqlite3")
CSV_PATH = "sample_data.csv"

conn = sqlite3.connect(DB_PATH)

# Skip if data already loaded
existing = conn.execute("SELECT COUNT(*) FROM lr_visual_completedata").fetchone()[0]
if existing > 0:
    print(f"Skipping: {existing} rows already in database.")
    conn.close()
else:
    df = pd.read_csv(CSV_PATH)
    df.to_sql("lr_visual_completedata", conn, if_exists="append", index=False)
    conn.close()
    print(f"Loaded {len(df)} rows from {CSV_PATH} into {DB_PATH}")
