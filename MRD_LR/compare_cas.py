import pandas as pd

def get_sample_cas(file_path):
    df = pd.read_csv(file_path, usecols=['CA_NO'], nrows=1000)
    return set(df['CA_NO'].tolist())

cas1 = get_sample_cas('FILE_FOR_VISUAL.csv')
cas2 = get_sample_cas('KT_FINAL_MERGED_JUNE_JULY.csv')

print(f"Sample CAs in FILE_FOR_VISUAL: {list(cas1)[:10]}...")
print(f"Sample CAs in KT_FINAL_MERGED: {list(cas2)[:10]}...")
print(f"Intersection size (first 1000): {len(cas1.intersection(cas2))}")
