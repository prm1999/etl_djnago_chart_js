import os
import django
import sys

# Setup Django environment
sys.path.append(r"e:\Asset Plus\Data_visual\MRD_LR")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MRD_LR.settings')
django.setup()

from lr_visual.models import completeData

def check_data():
    total_rows = completeData.objects.count()
    print(f"Total rows in completeData: {total_rows}")
    
    months = completeData.objects.values_list('MONTH', flat=True).distinct()
    print(f"Months present: {list(months)}")
    
    # Check for specific files if possible. 
    # Usually we can check by month. 
    # KT_FINAL_MERGED_JUNE_JULY likely contains June and July.
    # Let's see row counts per month.
    from django.db.models import Count
    month_counts = completeData.objects.values('MONTH').annotate(count=Count('id')).order_by('MONTH')
    for mc in month_counts:
        print(f"  {mc['MONTH']}: {mc['count']} rows")

if __name__ == "__main__":
    check_data()
