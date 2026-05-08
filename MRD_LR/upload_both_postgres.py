import os
import sys
import django
import pandas as pd
from sqlalchemy import create_engine

# Setup Django
sys.path.append(r"e:\Asset Plus\Data_visual\MRD_LR")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MRD_LR.settings')
django.setup()

from lr_visual.models import completeData

# Use SQLAlchemy for fast chunked inserts to PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:admin@localhost:5432/lr_visual')

def clean_kwh(val):
    if pd.isna(val):
        return 0.0
    if isinstance(val, str):
        return float(val.replace(',', ''))
    return float(val)

def upload_both():
    print("Clearing existing data to avoid triplication...")
    completeData.objects.all().delete()
    print("Existing data cleared.")

    file1 = 'FILE_FOR_VISUAL.csv'
    file2 = 'KT_FINAL_MERGED_JUNE_JULY.csv'
    chunk_size = 50000
    
    # 1. Upload FILE_FOR_VISUAL.csv
    print(f"\n--- Uploading {file1} ---")
    total1 = 0
    try:
        for chunk in pd.read_csv(file1, chunksize=chunk_size, low_memory=False, index_col=0):
            chunk.to_sql('lr_visual_completedata', engine, if_exists='append', index=False)
            total1 += len(chunk)
            print(f"  Inserted {total1} rows...")
    except Exception as e:
        print(f"Error uploading {file1}: {e}")

    # 2. Upload KT_FINAL_MERGED_JUNE_JULY.csv
    print(f"\n--- Uploading {file2} ---")
    col_mapping = {
        'MONTH': 'MONTH', 'YEAR': 'YEAR', 'CA_NO': 'CA_NO', 'MTR_NO': 'MTR_NO',
        'ZONE_NAME': 'ZONE_NAME', 'REGION': 'REGION', 'REGIO_GROUP': 'UNIT_CODE', 
        'ACC_CLASS': 'ACC_CLASS', 'SUB_DIVISION': 'SUB_DIVISION', 'TAMPER_COUNT': 'TAMPER_COUNT',
        'KWH': 'KWH', 'PAY_AGAINST_CURR_DMD': 'PAY_AGAINST_CURR_DMD', 
        'PAY_AGAINST_ARREARS': 'PAY_AGAINST_ARREARS', 'PAYMENT_AGAINSTTOTAL': 'PAYMENT_AGAINST_TOTAL', 
        'BUCKETING_DERIVED': 'BUCKETING_DERIVED', 'BUCKETING_DISPLAY': 'BUCKETING_DISPLAY'
    }
    
    total2 = 0
    try:
        for chunk in pd.read_csv(file2, usecols=list(col_mapping.keys()), chunksize=chunk_size, low_memory=False):
            chunk = chunk.rename(columns=col_mapping)
            
            # Clean KWH commas reliably
            chunk['KWH'] = chunk['KWH'].apply(clean_kwh)
                
            # Clean any NULLs for required float/int columns
            not_null_cols = ['YEAR', 'CA_NO', 'MTR_NO', 'TAMPER_COUNT', 'KWH', 'PAY_AGAINST_CURR_DMD', 'PAY_AGAINST_ARREARS', 'PAYMENT_AGAINST_TOTAL']
            for col in not_null_cols:
                if col in chunk.columns:
                    chunk[col] = chunk[col].fillna(0)
                    
            db_cols = list(col_mapping.values())
            chunk = chunk[db_cols]
            chunk.to_sql('lr_visual_completedata', engine, if_exists='append', index=False)
            total2 += len(chunk)
            print(f"  Inserted {total2} rows...")
    except Exception as e:
        print(f"Error uploading {file2}: {e}")
        
    # Final count check
    final_count = completeData.objects.count()
    print(f"\n--- Upload Complete! ---")
    print(f"Total rows in PostgreSQL database: {final_count}")

if __name__ == '__main__':
    upload_both()
