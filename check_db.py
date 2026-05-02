import os, django, sys

os.chdir(r"e:\Asset Plus\payment\CORE")
sys.path.insert(0, r"e:\Asset Plus\payment\CORE")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CORE.settings')
django.setup()

from django.db import connection
cursor = connection.cursor()

print("=" * 65)
print("   PBA PAGE (Payment Behavior Analysis) - DATA CHECK")
print("=" * 65)

# The PBA view uses PAYMENT_INSIGHT_SUMMARY and PAYMENT_BEHAVIOR_PREDICTION_DATA
print("\n[1] PaymentApp_payment_insight_summary - row count:")
cursor.execute('SELECT COUNT(*) FROM "PaymentApp_payment_insight_summary"')
print(f"    Rows: {cursor.fetchone()[0]}")

print("\n[2] PaymentApp_payment_behavior_prediction_data - row count:")
cursor.execute('SELECT COUNT(*) FROM "PaymentApp_payment_behavior_prediction_data"')
print(f"    Rows: {cursor.fetchone()[0]}")

# Check what the PMA view uses - PAYMENT_MODE and PAYMENT_MODE_PREDICTION
print("\n[3] PaymentApp_payment_mode - row count & sample:")
cursor.execute('SELECT COUNT(*) FROM "PaymentApp_payment_mode"')
print(f"    Rows: {cursor.fetchone()[0]}")
cursor.execute('SELECT * FROM "PaymentApp_payment_mode" LIMIT 5')
cols = [desc[0] for desc in cursor.description]
print(f"    Columns: {cols}")
for r in cursor.fetchall():
    print(f"    {r}")

print("\n[4] PaymentApp_payment_mode_prediction - row count & sample:")
cursor.execute('SELECT COUNT(*) FROM "PaymentApp_payment_mode_prediction"')
print(f"    Rows: {cursor.fetchone()[0]}")
cursor.execute('SELECT * FROM "PaymentApp_payment_mode_prediction" LIMIT 5')
cols = [desc[0] for desc in cursor.description]
print(f"    Columns: {cols}")
for r in cursor.fetchall():
    print(f"    {r}")

# Also check staticVar YEAR_LIST to understand FY mapping
print("\n[5] Checking staticVar YEAR_LIST and FY mapping...")
from PaymentApp.staticVar import YEAR_LIST, DIVISION_DICT, REGION_LIST
print(f"    YEAR_LIST: {YEAR_LIST}")
print(f"    REGION_LIST: {REGION_LIST}")
print(f"    DIVISION_DICT keys: {list(DIVISION_DICT.keys())}")
for k, v in DIVISION_DICT.items():
    print(f"      {k}: {v}")

print("\n" + "=" * 65)
