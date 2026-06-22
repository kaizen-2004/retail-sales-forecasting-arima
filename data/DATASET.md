# Dataset: UCI Online Retail

## Source
**Repository:** UCI Machine Learning Repository  
**URL:** https://archive.ics.uci.edu/ml/datasets/online+retail  
**Paper:** Daqing Chen, Sai Liang Sain, and Kun Guo, "Data mining for the online retail industry: A case study of RFM model-based customer segmentation using data mining", Journal of Database Marketing & Customer Strategy Management, Vol. 19, No. 3, pp. 197-208, 2012.

## Overview
This is a transactional dataset which contains all the transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail. The company mainly sells unique all-occasion gifts.

## File
**Online Retail.xlsx** - Single Excel file

| Column | Description |
|--------|-------------|
| InvoiceNo | Invoice number (6-digit unique identifier). Prefix 'C' indicates cancellation |
| StockCode | Product code (5-digit unique identifier) |
| Description | Product name |
| Quantity | Quantity of each product per transaction (negative for cancellations) |
| InvoiceDate | Date and time of invoice generation |
| UnitPrice | Unit price (sterling) |
| CustomerID | Customer number (5-digit unique identifier) |
| Country | Country name of the customer |

## Data Statistics
- **Records:** 541,909 transactions
- **Date Range:** December 1, 2010 - December 9, 2011 (~1 year)
- **Countries:** 38 (UK, Germany, France, EIRE, Spain, etc.)
- **Unique Products:** 4,070
- **Unique Customers:** 4,372
- **Unique Invoices:** 25,900

## Data Quality Notes
- **Missing Values:** ~25% of CustomerID values are missing (need to filter)
- **Negative Quantities:** Represent cancelled orders or returns
- **Negative UnitPrice:** Rare, likely data entry errors
- **Duplicates:** Some rows are duplicated (remove exact matches)
- **Outliers:** Very high quantities or prices may be bulk orders or errors

## Business Characteristics
- **Business Model:** UK B2B wholesale (not consumer retail)
- **Trading Days:** Monday-Friday only
- **Saturday:** No trading (closed for B2B wholesale)
- **Sunday:** No trading (closed for B2B wholesale)
- **Implication:** Time series has gaps on weekends - expected behavior, not missing data

## Usage in Project
1. Store raw Excel file in `data/raw/`
2. Convert to CSV for faster processing in Sprint 2
3. Filter: remove cancelled orders, missing CustomerIDs
4. Aggregate by date for time series forecasting
5. Focus on UK market or aggregate globally

## Analysis Opportunities
- **Time Series:** Daily/weekly/monthly sales forecasting
- **Customer Segmentation:** RFM analysis
- **Product Analysis:** Top products, categories
- **Geographic:** Sales by country
- **Seasonality:** Holiday patterns (Christmas spike)

## Citation
If using this dataset, cite:
> Chen, D., Sain, S.L., and Guo, K. (2012), "Data mining for the online retail industry: A case study of RFM model-based customer segmentation using data mining", Journal of Database Marketing & Customer Strategy Management, Vol. 19, No. 3, pp. 197-208.
