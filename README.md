# Sales Forecasting Analysis

A retail sales forecasting project using Python, Pandas, NumPy, Matplotlib, Statsmodels, and SQL.

## Project Overview
Build a sales forecasting system to process online retail sales data (~541K records), detect trends and seasonality, and create ARIMA forecasting models with interactive visualizations for inventory planning.

## Dataset
**UCI Online Retail Dataset**  
- UK-based online retailer (Dec 2010 - Dec 2011)  
- 541K transactions, 4,372 customers, 4,070 products  
- Features: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country  
- **Note:** B2B wholesale - no trading on weekends (Saturday/Sunday)

**Download:** See [data/DATASET.md](data/DATASET.md) for instructions

## Visualizations

### Sales Distribution & Top Countries
![Sales Distribution](reports/screenshots/01_sales_distribution.png)

### Daily Sales with Moving Averages & Day of Week Analysis
![Daily Sales Features](reports/screenshots/02_daily_sales_features.png)

## Quick Start

```bash
# 1. Clone the repository
git clone <repo-url>
cd sales-forecasting

# 2. Activate existing virtual environment and install dependencies
source ~/data-tools/bin/activate
uv pip install -e ".[dev]"

# 3. Place dataset
# Download from: https://archive.ics.uci.edu/ml/datasets/online+retail
# Extract to: data/raw/Online Retail.xlsx

# 4. Run Jupyter notebooks
jupyter notebook notebooks/
```

## Project Structure
```
sales-forecasting/
├── data/
│   ├── raw/              # Original UCI data
│   ├── processed/        # Cleaned data
│   └── DATASET.md        # Dataset documentation
├── notebooks/            # Jupyter analysis notebooks
│   ├── 01_EDA.ipynb      # Exploratory data analysis
│   └── 02_Data_Processing.ipynb  # Data processing pipeline
├── src/                  # Python modules
│   ├── data_processing.py
│   ├── feature_engineering.py
│   ├── validation.py
│   └── utils.py
├── config/               # Configuration files
├── reports/
│   ├── figures/          # Generated plots
│   └── screenshots/      # Documentation screenshots
├── tests/                # Unit tests
├── pyproject.toml        # Project configuration (uv/pip)
└── IMPLEMENTATION_PLAN.md
```

## Tech Stack
- **Language:** Python 3.9+
- **Package Manager:** uv (fast Python package installer)
- **Data Processing:** Pandas, NumPy
- **Database:** SQLite
- **Modeling:** Statsmodels (ARIMA)
- **Visualization:** Matplotlib, Seaborn, Plotly
- **Testing:** Pytest

## Development

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Activate environment and install
source ~/data-tools/bin/activate
uv pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=term-missing
```

## Implementation Plan
See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for agile sprint milestones.

## Citation
Chen, D., Sain, S.L., and Guo, K. (2012), "Data mining for the online retail industry", Journal of Database Marketing & Customer Strategy Management.
