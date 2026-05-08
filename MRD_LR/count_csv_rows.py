import pandas as pd
import os

files = ['FILE_FOR_VISUAL.csv', 'KT_FINAL_MERGED_JUNE_JULY.csv']
for f in files:
    if os.path.exists(f):
        # Count rows without loading the whole file
        count = 0
        for chunk in pd.read_csv(f, chunksize=100000, low_memory=False):
            count += len(chunk)
        print(f"{f}: {count} rows")
    else:
        print(f"{f} not found")
