import pandas as pd

def get_kwh_sum(file_path):
    s = 0
    # For KT file, find KWH col. It might be 'KWH' or something else.
    df_head = pd.read_csv(file_path, nrows=10)
    kwh_col = 'KWH' if 'KWH' in df_head.columns else None
    
    if kwh_col:
        for chunk in pd.read_csv(file_path, chunksize=100000, low_memory=False):
            # Clean KWH if it's string
            if chunk[kwh_col].dtype == 'object':
                chunk[kwh_col] = chunk[kwh_col].str.replace(',', '').astype(float)
            s += chunk[kwh_col].sum()
    return s

sum1 = get_kwh_sum('FILE_FOR_VISUAL.csv')
sum2 = get_kwh_sum('KT_FINAL_MERGED_JUNE_JULY.csv')

print(f"FILE_FOR_VISUAL KWH sum: {sum1}")
print(f"KT_FINAL_MERGED KWH sum: {sum2}")
