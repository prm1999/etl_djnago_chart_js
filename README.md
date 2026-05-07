# Customer Payment Analytics Dashboard

A Django-based analytics web application that processes large-scale electricity utility customer data and renders interactive dashboards for payment behavior analysis across billing zones.

Built to analyze 350,000+ meter records — the app runs ETL pipelines on raw CSV data, stores it in a relational database, and exposes filterable visualizations to business stakeholders.

---

## Features

- **5 Chart Types** — Bar, Pie, Drill-Down (zone → payment category), and Defaulter Hue charts, all rendered client-side via Highcharts.js
- **Multi-filter Dashboard** — filter by month (multi-select), billing zone, payment bucket category, and defaulter count threshold
- **Defaulter Analysis** — identify customers consistently defaulting across multiple months using count-based filtering
- **ETL Pipeline** — chunked CSV ingestion (50,000 rows/batch) to safely load 190 MB+ files without memory overflow
- **Dual Database Support** — SQLite for local development, PostgreSQL for production

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Django 3.2 |
| Data Processing | Pandas, Django-Pandas, SQLAlchemy |
| Frontend | HTML5, Bootstrap 5, JavaScript, Highcharts.js |
| Database | SQLite (dev) / PostgreSQL (prod) |

## Project Structure

```
etl_djnago_chart_js/
├── MRD_LR/
│   ├── lr_visual/
│   │   ├── templates/        # 8 HTML templates (one per chart type)
│   │   ├── models.py         # completeData model (17 fields, 350k+ rows)
│   │   ├── views.py          # 6 function-based views with ORM aggregation
│   │   ├── urls.py
│   │   └── staticVar.py      # Month, zone, and bucket configuration
│   ├── MRD_LR/
│   │   └── settings.py
│   ├── manage.py
│   └── requirements.txt
├── upload_sqlite.py          # Bulk CSV loader for SQLite
├── upload_second_csv.py      # Chunked CSV loader for large files (190 MB)
└── check_db.py               # Database inspection utility
```

## Local Setup

**1. Clone and create virtual environment**
```bash
git clone https://github.com/prm1999/etl_djnago_chart_js.git
cd etl_djnago_chart_js
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # Linux/Mac
```

**2. Install dependencies**
```bash
pip install -r MRD_LR/requirements.txt
```

**3. Set environment variable for secret key**
```bash
# Windows PowerShell
$env:DJANGO_SECRET_KEY = "your-secret-key-here"

# Linux/Mac
export DJANGO_SECRET_KEY="your-secret-key-here"
```

**4. Run migrations**
```bash
cd MRD_LR
python manage.py migrate
```

**5. Load data**

For a quick demo using the included sample data (30 records across 3 months and 4 zones):
```bash
cd ..
python load_sample_data.py
```

To load your own full dataset (~350k records):
```bash
python upload_sqlite.py          # small file (~48 MB)
python upload_second_csv.py      # large file (~190 MB), chunked
```

**6. Start the server**
```bash
cd MRD_LR
python manage.py runserver 8000
```

Visit `http://127.0.0.1:8000/`

## PostgreSQL Setup (Production)

Update `MRD_LR/MRD_LR/settings.py` to switch the `DATABASES` block:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lr_visual',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then load data directly via SQLAlchemy:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:<password>@localhost:5432/lr_visual')
for chunk in pd.read_csv('data.csv', chunksize=50000):
    chunk.to_sql('lr_visual_completedata', engine, if_exists='append', index=False)
```

## Data Schema

The `completeData` model captures electricity meter and billing records:

| Field | Description |
|---|---|
| `CA_NO` | Customer account number |
| `MTR_NO` | Meter number |
| `ZONE_NAME` | Billing zone (4 zones) |
| `MONTH` | Billing month |
| `KWH` | Units consumed |
| `CURRENT_DEMAND` | Current bill amount |
| `ARREAR_AMOUNT` | Outstanding dues |
| `BUCKETING_DERIVED` | Payment category (Defaulter, On-time, etc.) |
| `BUCKETING_DISPLAY` | Human-readable payment bucket label |

---

Developed by [Pradeep](https://github.com/prm1999)
