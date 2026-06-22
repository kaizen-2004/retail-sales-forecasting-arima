"""
Feature engineering module for time series forecasting.
"""

import pandas as pd
import numpy as np


def add_time_features(df: pd.DataFrame, date_column: str = "Date") -> pd.DataFrame:
    """
    Add time-based features to the dataframe.
    
    Args:
        df: DataFrame with date column
        date_column: Name of the date column
        
    Returns:
        DataFrame with added time features
    """
    df = df.copy()
    
    # Ensure datetime
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Basic time features
    df["year"] = df[date_column].dt.year
    df["month"] = df[date_column].dt.month
    df["day"] = df[date_column].dt.day
    df["day_of_week"] = df[date_column].dt.dayofweek  # Monday=0, Sunday=6
    df["day_of_year"] = df[date_column].dt.dayofyear
    df["week_of_year"] = df[date_column].dt.isocalendar().week.astype(int)
    df["quarter"] = df[date_column].dt.quarter
    
    # Is weekend flag
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
    
    # Month names
    df["month_name"] = df[date_column].dt.month_name()
    df["day_name"] = df[date_column].dt.day_name()
    
    return df


def add_lag_features(df: pd.DataFrame, column: str, lags: list[int]) -> pd.DataFrame:
    """
    Add lag features for time series.
    
    Args:
        df: DataFrame sorted by date
        column: Column to create lags for
        lags: List of lag periods
        
    Returns:
        DataFrame with lag features
    """
    df = df.copy()
    for lag in lags:
        df[f"{column}_lag_{lag}"] = df[column].shift(lag)
    return df


def add_rolling_features(
    df: pd.DataFrame, 
    column: str, 
    windows: list[int]
) -> pd.DataFrame:
    """
    Add rolling window features.
    
    Args:
        df: DataFrame sorted by date
        column: Column to calculate rolling stats for
        windows: List of window sizes
        
    Returns:
        DataFrame with rolling features
    """
    df = df.copy()
    for window in windows:
        df[f"{column}_rolling_mean_{window}"] = df[column].rolling(window=window).mean()
        df[f"{column}_rolling_std_{window}"] = df[column].rolling(window=window).std()
    return df


def add_expanding_features(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Add expanding window features (cumulative stats).
    
    Args:
        df: DataFrame sorted by date
        column: Column to calculate expanding stats for
        
    Returns:
        DataFrame with expanding features
    """
    df = df.copy()
    df[f"{column}_expanding_mean"] = df[column].expanding().mean()
    df[f"{column}_expanding_std"] = df[column].expanding().std()
    return df


def create_forecast_features(
    df: pd.DataFrame,
    date_column: str = "Date",
    target_column: str = "total_sales",
    lags: list[int] | None = None,
    windows: list[int] | None = None,
) -> pd.DataFrame:
    """
    Create all features needed for forecasting.
    
    Args:
        df: DataFrame with date and target columns
        date_column: Name of the date column
        target_column: Name of the target column
        lags: List of lag periods (default: [1, 7, 14, 28])
        windows: List of rolling window sizes (default: [7, 14, 28])
        
    Returns:
        DataFrame with all features
    """
    if lags is None:
        lags = [1, 7, 14, 28]
    if windows is None:
        windows = [7, 14, 28]
    
    # Sort by date
    df = df.sort_values(date_column).reset_index(drop=True)
    
    # Add time features
    df = add_time_features(df, date_column)
    
    # Add lag features
    df = add_lag_features(df, target_column, lags)
    
    # Add rolling features
    df = add_rolling_features(df, target_column, windows)
    
    # Add expanding features
    df = add_expanding_features(df, target_column)
    
    return df
