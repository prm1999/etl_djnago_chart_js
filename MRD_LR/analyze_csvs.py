import pandas as pd
import os

def check_csv(file_path):
    print(f"Checking {file_path}...")
    try:
        # For KT_FINAL_MERGED_JUNE_JULY, the month column name might be 'MONTH' or something else
        # Let's check columns first
        df_head = pd.read_csv(file_path, nrows=0)
        cols = df_head.columns.tolist()
        print(f"  Columns: {cols[:10]}...")
        
        # Determine month column
        month_col = 'MONTH' if 'MONTH' in cols else ('BILLMONTH' if 'BILLMONTH' in cols else None)
        
        if month_col:
            count = 0
            month_dist = {}
            for chunk in pd.read_csv(file_path, chunksize=100000, low_memory=False):
                count += len(chunk)
                m_counts = chunk[month_col].value_counts()
                for m, c in m_counts.items():
                    month_dist[m] = month_dist.get(m, 0) + c
            print(f"  Total rows: {count}")
            print(f"  Month distribution: {month_dist}")
        else:
            print("  Month column not found")
    except Exception as e:
        print(f"  Error checking {file_path}: {e}")

check_csv('FILE_FOR_VISUAL.csv')
print("-" * 30)
check_csv('KT_FINAL_MERGED_JUNE_JULY.csv')
