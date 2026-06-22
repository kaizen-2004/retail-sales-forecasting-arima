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

**What question does this answer?**
> "How much do customers typically spend per order?"

**What the chart shows:**
- Most orders are small — under £50
- A few very large orders (over £1,000) skew the average higher
- Typical order is around £12, but the average is £22 because of those big orders

**Why it matters:**
This is a B2B wholesaler, not a regular retail store. Small orders are routine restocks from regular customers. The big orders are likely bulk purchases from other retailers. Knowing this helps with inventory planning and pricing strategies.

---

### 2. Top 10 Countries by Sales

**What question does this answer?**
> "Where are our biggest customers located?"

**What the chart shows:**
- United Kingdom accounts for about 80% of all sales
- Ireland and Germany are distant second and third
- We sell to 37 countries, but most revenue comes from just a few

**Why it matters:**
The business is heavily dependent on the UK market. This is both a strength (strong home market) and a risk (if UK economy slows, sales suffer). There's room to grow in other European countries, but it would require understanding local markets.

---

### 3. Daily Sales with Moving Averages

![Daily Sales Features](reports/screenshots/02_daily_sales_features.png)

**What question does this answer?**
> "Are sales going up or down over time, and can we spot patterns?"

**What the chart shows:**
- The jagged line is daily sales — very volatile day-to-day
- The smooth lines are moving averages (7-day and 28-day) that show the real trend
- Clear spikes around holidays (Christmas, Black Friday)
- No sales on weekends — this is a business-to-business operation

**Why it matters:**
Moving averages help us see through the daily noise. The 28-day trend line is what you'd use for inventory planning — it shows where sales are heading without getting distracted by random daily fluctuations. The holiday spikes tell us when to stock up.

---

### 4. Average Sales by Day of Week

**What question does this answer?**
> "Which days are busiest, and when should we focus our efforts?"

**What the chart shows:**
- Thursday is the biggest sales day
- Tuesday is also strong
- Saturday has zero sales (closed)
- Sunday has very little activity

**Why it matters:**
Customers tend to order early in the week and again before the weekend. Thursday being the peak suggests businesses are restocking before Friday. This pattern helps with staffing, promotions, and when to launch marketing campaigns.

---

## Key Takeaways

| What We Found | What It Means |
|---------------|---------------|
| Most orders are small (< £50) | Focus on high-volume, low-value inventory |
| UK is 80% of revenue | Diversify to reduce market risk |
| Thursday is the busiest day | Staff up and run promotions mid-week |
| Clear holiday spikes | Stock up 2-3 weeks before major holidays |
| No weekend sales | B2B model — weekends can be low-priority |

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
