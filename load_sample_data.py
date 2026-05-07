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

df = pd.read_csv(CSV_PATH)
conn = sqlite3.connect(DB_PATH)
df.to_sql("lr_visual_completedata", conn, if_exists="append", index=False)
conn.close()

print(f"Loaded {len(df)} rows from {CSV_PATH} into {DB_PATH}")
