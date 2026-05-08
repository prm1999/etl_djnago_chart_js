import os
import sys
import django
import pandas as pd

sys.path.append(r"e:\Asset Plus\Data_visual\MRD_LR")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MRD_LR.settings')
django.setup()

from lr_visual.models import completeData

def verify():
    print("--- POSTGRESQL DATABASE VERIFICATION ---")
    
    # 1. Total count
    total_db = completeData.objects.count()
    print(f"\n1. Total Rows in Postgres DB: {total_db}")
    
    # 2. Month breakdown
    from django.db.models import Count
    months = completeData.objects.values('MONTH').annotate(c=Count('id'))
    print("\n2. Postgres Month Breakdown:")
    for m in months:
        print(f"  {m['MONTH']}: {m['c']}")
        
    # 3. Check for duplicates
    # If the user uploaded BOTH files (which contain the same records),
    # there would be duplicate CA_NO entries for the same month.
    print("\n3. Checking for duplicates (Did we upload BOTH files?)...")
    
    # Get total number of distinct CA_NO + MONTH combinations
    distinct_combinations = completeData.objects.values('MONTH', 'CA_NO').distinct().count()
    print(f"  Total distinct (MONTH, CA_NO) combinations: {distinct_combinations}")
    
    if distinct_combinations == total_db:
         print("  -> Conclusion: Every record is unique. Only ONE file's data was uploaded.")
    elif total_db == distinct_combinations * 2:
         print("  -> Conclusion: Every record appears exactly twice. BOTH files were uploaded.")
    else:
         print(f"  -> Conclusion: There are duplicates, but not exactly double. Difference: {total_db - distinct_combinations}")

if __name__ == '__main__':
    verify()
