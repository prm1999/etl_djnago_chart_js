# ETL Django Chart Visualization (MRD LR)

A Django-based data visualization platform that processes large-scale customer data and presents it through interactive charts (Pie Charts, Drill-downs, and Hues). The project leverages `django-pandas` for efficient data manipulation and supports both SQLite and PostgreSQL.

## 🚀 Features

- **Interactive Dashboards**: Dynamic visualizations including Pie Charts and Drill-down charts.
- **Data Filtering**: Filter data by Month and Zone for granular analysis.
- **Efficient Data Processing**: Uses `pandas` for handling large datasets (up to 350k+ rows).
- **Multiple DB Support**: Configurable for both SQLite (local development) and PostgreSQL (production).

## 🛠️ Tech Stack

- **Backend**: Python 3.11, Django 3.2
- **Data Processing**: Pandas, Django-Pandas
- **Frontend**: HTML5, Vanilla CSS, JavaScript, Highcharts/Chart.js
- **Database**: PostgreSQL (configured) / SQLite

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL (if using the production configuration)
- Virtual Environment (`venv`)

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/prm1999/etl_djnago_chart_js.git
   cd etl_djnago_chart_js
   ```

2. **Create and Activate Virtual Environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r MRD_LR/requirements.txt
   pip install sqlalchemy  # For data upload scripts
   ```

4. **Database Configuration**:
   Update `MRD_LR/MRD_LR/settings.py` with your PostgreSQL credentials.

5. **Run Migrations**:
   ```bash
   python MRD_LR/manage.py migrate
   ```

## 📊 Data Ingestion

To upload your CSV data to the database, you can use a script like this:

```python
import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('FILE_FOR_VISUAL.csv')
engine = create_engine('postgresql://postgres:admin@localhost:5432/lr_visual')
df.to_sql('lr_visual_completedata', engine, if_exists='append', index=False)
```

## 🚀 Running the App

```bash
cd MRD_LR
python manage.py runserver 8000
```
Visit `http://127.0.0.1:8000/` in your browser.

## 📁 Project Structure

- `MRD_LR/`: Main Django project folder.
- `lr_visual/`: Main application folder containing views for charts.
- `templates/`: HTML templates for different visualization types.
- `staticVar.py`: Configuration for months and zones.

---
Developed by [Pradeep](https://github.com/prm1999)
