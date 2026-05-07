import pandas as pd
import sqlite3
import time

def upload_second_file():
    start_time = time.time()
    db_path = r"c:\Users\2118305\Documents\old_project\etl_djnago_chart_js\MRD_LR\db.sqlite3"
    csv_path = r"c:\Users\2118305\Documents\old_project\etl_djnago_chart_js\KT_FINAL_MERGED_JUNE_JULY.csv"
    
    print(f"Connecting to SQLite...")
    conn = sqlite3.connect(db_path)
    
    # We only want to keep the columns that match the database model
    # Model: id, MONTH, YEAR, CA_NO, MTR_NO, ZONE_NAME, REGION, UNIT_CODE, ACC_CLASS, SUB_DIVISION, TAMPER_COUNT, KWH, PAY_AGAINST_CURR_DMD, PAY_AGAINST_ARREARS, PAYMENT_AGAINST_TOTAL, BUCKETING_DERIVED, BUCKETING_DISPLAY
    
    # Mapping for the second CSV file:
    col_mapping = {
        'MONTH': 'MONTH',
        'YEAR': 'YEAR',
        'CA_NO': 'CA_NO',
        'MTR_NO': 'MTR_NO',
        'ZONE_NAME': 'ZONE_NAME',
        'REGION': 'REGION',
        'REGIO_GROUP': 'UNIT_CODE', # From Migration 0003
        'ACC_CLASS': 'ACC_CLASS',
        'SUB_DIVISION': 'SUB_DIVISION',
        'TAMPER_COUNT': 'TAMPER_COUNT',
        'KWH': 'KWH',
        'PAY_AGAINST_CURR_DMD': 'PAY_AGAINST_CURR_DMD',
        'PAY_AGAINST_ARREARS': 'PAY_AGAINST_ARREARS',
        'PAYMENT_AGAINSTTOTAL': 'PAYMENT_AGAINST_TOTAL', # Typo in CSV
        'BUCKETING_DERIVED': 'BUCKETING_DERIVED',
        'BUCKETING_DISPLAY': 'BUCKETING_DISPLAY'
    }
    
    print(f"Reading data from {csv_path} in chunks...")
    # Use chunksize to read the large file efficiently without taking up too much RAM
    chunk_size = 50000
    total_inserted = 0
    
    # Read the CSV with only the needed columns
    for chunk in pd.read_csv(csv_path, usecols=list(col_mapping.keys()), chunksize=chunk_size, low_memory=False):
        # Rename columns to match database schema
        chunk = chunk.rename(columns=col_mapping)
        
        # Clean data types if necessary (e.g. converting KWH strings with commas to float)
        if chunk['KWH'].dtype == 'object':
            chunk['KWH'] = chunk['KWH'].str.replace(',', '').astype(float)
            
        # Fill NA for NOT NULL columns
        not_null_cols = ['YEAR', 'CA_NO', 'MTR_NO', 'TAMPER_COUNT', 'KWH', 'PAY_AGAINST_CURR_DMD', 'PAY_AGAINST_ARREARS', 'PAYMENT_AGAINST_TOTAL']
        for col in not_null_cols:
            if col in chunk.columns:
                chunk[col] = chunk[col].fillna(0)
            
        # Ensure correct column order
        db_cols = list(col_mapping.values())
        chunk = chunk[db_cols]
        
        # Insert to database
        chunk.to_sql('lr_visual_completedata', conn, if_exists='append', index=False, chunksize=10000)
        total_inserted += len(chunk)
        print(f"Inserted {total_inserted} rows...")
        
    conn.close()
    
    end_time = time.time()
    print(f"Upload complete in {end_time - start_time:.2f} seconds. Total rows appended: {total_inserted}")

if __name__ == '__main__':
    upload_second_file()
