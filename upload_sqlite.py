import pandas as pd
import sqlite3
import time
import os

def upload_fast():
    start_time = time.time()
    db_path = r"c:\Users\2118305\Documents\old_project\etl_djnago_chart_js\MRD_LR\db.sqlite3"
    csv_path = r"c:\Users\2118305\Documents\old_project\etl_djnago_chart_js\FILE_FOR_VISUAL.csv"
    
    print(f"Loading data from {csv_path}...")
    # Read the CSV. The first column seems to be an unnamed index, so we can ignore it
    df = pd.read_csv(csv_path, index_col=0)
    
    # Ensure column names match the model exactly.
    # The model columns are:
    # id, MONTH, YEAR, CA_NO, MTR_NO, ZONE_NAME, REGION, UNIT_CODE, ACC_CLASS, SUB_DIVISION, TAMPER_COUNT, KWH, PAY_AGAINST_CURR_DMD, PAY_AGAINST_ARREARS, PAYMENT_AGAINST_TOTAL, BUCKETING_DERIVED, BUCKETING_DISPLAY
    
    print("Connecting to SQLite...")
    conn = sqlite3.connect(db_path)
    
    print("Uploading data efficiently...")
    # method='multi' is faster, but since SQLite has limits, chunksize is important
    df.to_sql('lr_visual_completedata', conn, if_exists='append', index=False, chunksize=10000)
    
    conn.close()
    
    end_time = time.time()
    print(f"Upload complete in {end_time - start_time:.2f} seconds.")

if __name__ == '__main__':
    upload_fast()
