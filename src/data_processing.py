"""
Data processing module for the Sales Forecasting project.
Handles data loading, cleaning, and transformation.
"""

import pandas as pd
from pathlib import Path


def load_excel_data(file_path: str | Path) -> pd.DataFrame:
    """
    Load data from Excel file.
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        pandas DataFrame with the loaded data
    """
    return pd.read_excel(file_path)


def get_data_info(df: pd.DataFrame) -> dict:
    """
    Get basic information about the dataset.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        Dictionary with dataset information
    """
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
    }


def filter_valid_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter out invalid transactions (cancelled orders, missing customer IDs).
    
    Args:
        df: Raw transaction data
        
    Returns:
        Filtered DataFrame with valid transactions only
    """
    # Remove cancelled orders (InvoiceNo starting with 'C')
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
    
    # Remove rows with missing CustomerID
    df = df.dropna(subset=["CustomerID"])
    
    # Convert CustomerID to integer
    df["CustomerID"] = df["CustomerID"].astype(int)
    
    # Remove negative quantities
    df = df[df["Quantity"] > 0]
    
    # Remove negative or zero prices
    df = df[df["UnitPrice"] > 0]
    
    return df


def add_sales_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a Sales column (Quantity * UnitPrice).
    
    Args:
        df: DataFrame with Quantity and UnitPrice columns
        
    Returns:
        DataFrame with added Sales column
    """
    df = df.copy()
    df["Sales"] = df["Quantity"] * df["UnitPrice"]
    return df


def aggregate_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate sales data by date.
    
    Args:
        df: Transaction-level DataFrame
        
    Returns:
        DataFrame with daily aggregated sales
    """
    # Ensure InvoiceDate is datetime
    df = df.copy()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    
    # Extract date only
    df["Date"] = df["InvoiceDate"].dt.date
    
    # Aggregate by date
    daily_sales = df.groupby("Date").agg(
        total_sales=("Sales", "sum"),
        transaction_count=("InvoiceNo", "nunique"),
        quantity_sold=("Quantity", "sum"),
        unique_customers=("CustomerID", "nunique"),
    ).reset_index()
    
    # Convert Date back to datetime
    daily_sales["Date"] = pd.to_datetime(daily_sales["Date"])
    
    # Sort by date
    daily_sales = daily_sales.sort_values("Date").reset_index(drop=True)
    
    return daily_sales
