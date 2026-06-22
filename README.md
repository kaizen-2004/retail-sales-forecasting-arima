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

---

## Exploratory Data Analysis

### 1. Transaction Sales Distribution

![Sales Distribution](reports/screenshots/01_sales_distribution.png)

**Business Question:** *What is the typical order value, and how are sales distributed across transactions?*

**Insights:**
- **Right-skewed distribution** — majority of transactions are small (< £50), with a long tail of large orders
- **Median transaction: ~£12** vs **Mean: ~£22** — outliers pull the average up
- **Bulk orders exist** — some transactions exceed £1,000, likely B2B wholesale purchases
- **Actionable insight:** Focus inventory on high-volume, low-value items; bulk pricing strategies for large orders

**Data Story:** The company operates as a B2B wholesaler — most orders are small replenishment purchases, but occasional large bulk orders from retailers significantly impact revenue.

---

### 2. Top 10 Countries by Sales

**Business Question:** *Where are our biggest markets, and should we focus expansion efforts?*

**Insights:**
- **United Kingdom dominates** (~80% of revenue) — home market is primary revenue driver
- **EIRE (Ireland)** and **Germany** are secondary markets
- **Long tail of countries** — 37 countries total, but top 3 account for majority of sales
- **Actionable insight:** Consider targeted marketing in secondary markets; investigate why UK concentration is so high

**Data Story:** The business is heavily UK-focused with some European penetration. International expansion opportunities exist but require understanding local market dynamics.

---

### 3. Daily Sales with Moving Averages

![Daily Sales Features](reports/screenshots/02_daily_sales_features.png)

**Business Question:** *What are the sales trends over time, and are there predictable patterns?*

**Insights:**
- **7-day moving average** smooths daily volatility — reveals underlying trend
- **28-day moving average** shows longer-term direction — useful for inventory planning
- **Seasonal spikes visible** — likely holiday periods (Christmas, Black Friday)
- **Weekday-only trading** — gaps on weekends confirm B2B model
- **Actionable insight:** Use 28-day MA for reorder timing; prepare inventory 2-3 weeks before predicted spikes

**Data Story:** Sales show clear weekly cycles and seasonal patterns. The moving averages help separate noise from signal, enabling better demand forecasting.

---

### 4. Average Sales by Day of Week

**Business Question:** *Which days generate the most revenue, and how should we staff/schedule?*

**Insights:**
- **Thursday peak** — highest average sales, possibly end-of-week restocking
- **Tuesday strong** — early-week ordering pattern
- **Saturday closed** — no trading (B2B wholesale model)
- **Sunday minimal** — some limited activity
- **Actionable insight:** Staff customer service and fulfillment teams heavily on Tuesday/Thursday; run promotions on slower days (Monday/Wednesday)

**Data Story:** The business follows a clear weekly rhythm — customers order early in the week and again before the weekend. Understanding this pattern helps optimize operations.

---

## Key Findings Summary

| Finding | Business Impact |
|---------|-----------------|
| Right-skewed sales distribution | Focus on high-volume items; bulk pricing for large orders |
| UK dominates revenue | Diversify markets; investigate international barriers |
| Weekly cycle (Thu peak) | Optimize staffing and promotions by day |
| Seasonal spikes | Pre-position inventory before holidays |
| B2B model (weekdays only) | Weekend operations can be minimal |

---

## Quick Start

```bash
# 1. Clone the repository
git clone git@github.com:kaizen-2004/retail-sales-forecasting-arima.git
cd retail-sales-forecasting-arima

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
