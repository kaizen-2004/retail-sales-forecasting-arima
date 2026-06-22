"""
Time series analysis module for trend and seasonality detection.
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.arima.model import ARIMA
from scipy import stats


def detect_trend(x: np.ndarray, y: np.ndarray) -> dict:
    """
    Detect linear trend in data.
    
    Args:
        x: Independent variable (e.g., time index)
        y: Dependent variable (e.g., sales)
        
    Returns:
        Dictionary with trend information
    """
    # Remove NaN values
    mask = ~np.isnan(y)
    x_clean, y_clean = x[mask], y[mask]
    
    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_clean, y_clean)
    
    # Determine trend direction
    if p_value < 0.05:  # Statistically significant
        if slope > 0:
            direction = "increasing"
        else:
            direction = "decreasing"
    else:
        direction = "no significant trend"
    
    return {
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_value ** 2,
        "p_value": p_value,
        "direction": direction,
        "interpretation": f"Sales are {direction} (p={p_value:.4f}, R²={r_value**2:.4f})"
    }


def check_stationarity(series: pd.Series) -> dict:
    """
    Check stationarity using ADF and KPSS tests.
    
    Args:
        series: Time series data
        
    Returns:
        Dictionary with stationarity test results
    """
    # Drop NaN values
    series_clean = series.dropna()
    
    # ADF test (null hypothesis: unit root exists, series is non-stationary)
    adf_result = adfuller(series_clean, autolag='AIC')
    
    # KPSS test (null hypothesis: series is stationary)
    kpss_result = kpss(series_clean, regression='c', nlags='auto')
    
    # Determine stationarity
    adf_stationary = adf_result[1] < 0.05  # Reject null = stationary
    kpss_stationary = kpss_result[1] > 0.05  # Fail to reject null = stationary
    
    if adf_stationary and kpss_stationary:
        conclusion = "Stationary"
    elif not adf_stationary and not kpss_stationary:
        conclusion = "Non-stationary"
    elif adf_stationary and not kpss_stationary:
        conclusion = "Inconclusive (ADF says stationary, KPSS says non-stationary)"
    else:
        conclusion = "Inconclusive (ADF says non-stationary, KPSS says stationary)"
    
    return {
        "adf_statistic": adf_result[0],
        "adf_p_value": adf_result[1],
        "adf_stationary": adf_stationary,
        "kpss_statistic": kpss_result[0],
        "kpss_p_value": kpss_result[1],
        "kpss_stationary": kpss_stationary,
        "conclusion": conclusion
    }


def decompose_time_series(
    series: pd.Series,
    period: int = 7,
    model: str = 'additive'
) -> dict:
    """
    Decompose time series into trend, seasonal, and residual components.
    
    Args:
        series: Time series data
        period: Seasonal period (7 for weekly, 30 for monthly)
        model: 'additive' or 'multiplicative'
        
    Returns:
        Dictionary with decomposition components
    """
    # Drop NaN values
    series_clean = series.dropna()
    
    # Perform decomposition
    decomposition = seasonal_decompose(series_clean, model=model, period=period)
    
    return {
        "trend": decomposition.trend,
        "seasonal": decomposition.seasonal,
        "residual": decomposition.resid,
        "observed": decomposition.observed,
        "period": period,
        "model": model
    }


def calculate_seasonal_strength(decomposition: dict) -> float:
    """
    Calculate the strength of seasonality.
    
    Args:
        decomposition: Output from decompose_time_series
        
    Returns:
        Seasonal strength (0-1, higher = stronger seasonality)
    """
    seasonal = decomposition["seasonal"].dropna()
    residual = decomposition["residual"].dropna()
    
    # Align indices
    common_idx = seasonal.index.intersection(residual.index)
    seasonal = seasonal[common_idx]
    residual = residual[common_idx]
    
    # Calculate variance ratio
    var_seasonal = np.var(seasonal)
    var_residual = np.var(residual)
    
    if var_seasonal + var_residual == 0:
        return 0.0
    
    strength = var_seasonal / (var_seasonal + var_residual)
    return strength


def identify_peak_periods(df: pd.DataFrame, date_col: str = "Date", value_col: str = "total_sales") -> dict:
    """
    Identify peak sales periods (daily, weekly, monthly patterns).
    
    Args:
        df: DataFrame with date and sales columns
        date_col: Name of date column
        value_col: Name of sales column
        
    Returns:
        Dictionary with peak period information
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Day of week pattern
    df["day_of_week"] = df[date_col].dt.dayofweek
    daily_pattern = df.groupby("day_of_week")[value_col].mean()
    
    # Monthly pattern
    df["month"] = df[date_col].dt.month
    monthly_pattern = df.groupby("month")[value_col].mean()
    
    # Find peaks
    peak_day = daily_pattern.idxmax()
    peak_month = monthly_pattern.idxmax()
    
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    return {
        "peak_day_of_week": day_names[peak_day],
        "peak_day_sales": daily_pattern[peak_day],
        "daily_pattern": daily_pattern,
        "peak_month": month_names[peak_month - 1],
        "peak_month_sales": monthly_pattern[peak_month],
        "monthly_pattern": monthly_pattern
    }


def calculate_autocorrelation(series: pd.Series, lags: int = 30) -> pd.DataFrame:
    """
    Calculate autocorrelation and partial autocorrelation.
    
    Args:
        series: Time series data
        lags: Number of lags to calculate
        
    Returns:
        DataFrame with ACF and PACF values
    """
    from statsmodels.tsa.stattools import acf, pacf
    
    series_clean = series.dropna()
    
    acf_values = acf(series_clean, nlags=lags, fft=True)
    pacf_values = pacf(series_clean, nlags=lags)
    
    return pd.DataFrame({
        "lag": range(lags + 1),
        "acf": acf_values,
        "pacf": pacf_values
    })
