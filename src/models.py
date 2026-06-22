"""
ARIMA/SARIMA forecasting module.
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')


def calculate_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict:
    """
    Calculate forecasting metrics.
    
    Args:
        actual: Actual values
        predicted: Predicted values
        
    Returns:
        Dictionary with MAPE, RMSE, MAE, MAE
    """
    # Remove NaN values
    mask = ~np.isnan(actual) & ~np.isnan(predicted)
    actual, predicted = actual[mask], predicted[mask]
    
    # MAPE (Mean Absolute Percentage Error)
    # Avoid division by zero by filtering out zero actual values
    non_zero_mask = actual != 0
    if non_zero_mask.sum() > 0:
        mape = np.mean(np.abs((actual[non_zero_mask] - predicted[non_zero_mask]) / actual[non_zero_mask])) * 100
    else:
        mape = np.inf
    
    # RMSE (Root Mean Squared Error)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    
    # MAE (Mean Absolute Error)
    mae = mean_absolute_error(actual, predicted)
    
    # MAPE using all values (with handling for zeros)
    mape_all = np.mean(np.abs((actual - predicted) / np.where(actual == 0, 1, actual))) * 100
    
    return {
        "mape": mape,
        "mape_all": mape_all,
        "rmse": rmse,
        "mae": mae,
        "actual_mean": np.mean(actual),
        "predicted_mean": np.mean(predicted)
    }


def train_test_split_time_series(
    series: pd.Series, 
    test_size: float = 0.2
) -> tuple[pd.Series, pd.Series]:
    """
    Split time series into train and test sets (time-aware).
    
    Args:
        series: Time series data
        test_size: Fraction of data for testing
        
    Returns:
        Tuple of (train, test) series
    """
    split_idx = int(len(series) * (1 - test_size))
    return series[:split_idx], series[split_idx:]


def fit_arima(
    train: pd.Series,
    order: tuple = (1, 1, 1),
    forecast_steps: int = None
) -> dict:
    """
    Fit ARIMA model and make predictions.
    
    Args:
        train: Training time series
        order: ARIMA order (p, d, q)
        forecast_steps: Number of steps to forecast (None = len of test)
        
    Returns:
        Dictionary with model, predictions, and metrics
    """
    # Fit model
    model = ARIMA(train, order=order)
    fitted_model = model.fit()
    
    # Make predictions
    if forecast_steps:
        predictions = fitted_model.forecast(steps=forecast_steps)
    else:
        predictions = fitted_model.fittedvalues
    
    return {
        "model": fitted_model,
        "predictions": predictions,
        "order": order,
        "aic": fitted_model.aic,
        "bic": fitted_model.bic
    }


def fit_sarima(
    train: pd.Series,
    order: tuple = (1, 1, 1),
    seasonal_order: tuple = (1, 1, 1, 7),
    forecast_steps: int = None
) -> dict:
    """
    Fit SARIMA model (Seasonal ARIMA) and make predictions.
    
    Args:
        train: Training time series
        order: ARIMA order (p, d, q)
        seasonal_order: Seasonal order (P, D, Q, s)
        forecast_steps: Number of steps to forecast
        
    Returns:
        Dictionary with model, predictions, and metrics
    """
    # Fit model
    model = SARIMAX(train, order=order, seasonal_order=seasonal_order)
    fitted_model = model.fit(disp=False)
    
    # Make predictions
    if forecast_steps:
        predictions = fitted_model.forecast(steps=forecast_steps)
    else:
        predictions = fitted_model.fittedvalues
    
    return {
        "model": fitted_model,
        "predictions": predictions,
        "order": order,
        "seasonal_order": seasonal_order,
        "aic": fitted_model.aic,
        "bic": fitted_model.bic
    }


def grid_search_arima(
    train: pd.Series,
    p_range: range = range(0, 3),
    d_range: range = range(0, 2),
    q_range: range = range(0, 3),
    max_mape: float = 100.0
) -> list[dict]:
    """
    Grid search for best ARIMA parameters.
    
    Args:
        train: Training time series
        p_range: Range of p parameters
        d_range: Range of d parameters
        q_range: Range of q parameters
        max_mape: Maximum acceptable MAPE
        
    Returns:
        List of results sorted by AIC
    """
    results = []
    
    for p in p_range:
        for d in d_range:
            for q in q_range:
                try:
                    # Fit model with cross-validation
                    split_idx = int(len(train) * 0.8)
                    train_cv = train[:split_idx]
                    val = train[split_idx:]
                    
                    result = fit_arima(train_cv, order=(p, d, q), forecast_steps=len(val))
                    metrics = calculate_metrics(val.values, result["predictions"].values)
                    
                    if metrics["mape"] < max_mape:
                        results.append({
                            "order": (p, d, q),
                            "aic": result["aic"],
                            "bic": result["bic"],
                            "mape": metrics["mape"],
                            "rmse": metrics["rmse"],
                            "mae": metrics["mae"]
                        })
                except Exception as e:
                    continue
    
    # Sort by AIC
    results.sort(key=lambda x: x["aic"])
    return results


def grid_search_sarima(
    train: pd.Series,
    p_range: range = range(0, 2),
    d_range: range = range(0, 2),
    q_range: range = range(0, 2),
    seasonal_period: int = 7,
    max_mape: float = 100.0
) -> list[dict]:
    """
    Grid search for best SARIMA parameters.
    
    Args:
        train: Training time series
        p_range: Range of p parameters
        d_range: Range of d parameters
        q_range: Range of q parameters
        seasonal_period: Seasonal period (7 for weekly)
        max_mape: Maximum acceptable MAPE
        
    Returns:
        List of results sorted by AIC
    """
    results = []
    
    for p in p_range:
        for d in d_range:
            for q in q_range:
                try:
                    # Fit model with cross-validation
                    split_idx = int(len(train) * 0.8)
                    train_cv = train[:split_idx]
                    val = train[split_idx:]
                    
                    result = fit_sarima(
                        train_cv, 
                        order=(p, d, q),
                        seasonal_order=(1, 1, 1, seasonal_period),
                        forecast_steps=len(val)
                    )
                    metrics = calculate_metrics(val.values, result["predictions"].values)
                    
                    if metrics["mape"] < max_mape:
                        results.append({
                            "order": (p, d, q),
                            "seasonal_order": (1, 1, 1, seasonal_period),
                            "aic": result["aic"],
                            "bic": result["bic"],
                            "mape": metrics["mape"],
                            "rmse": metrics["rmse"],
                            "mae": metrics["mae"]
                        })
                except Exception as e:
                    continue
    
    # Sort by AIC
    results.sort(key=lambda x: x["aic"])
    return results


def create_forecast_dataframe(
    actual: pd.Series,
    train_predictions: pd.Series,
    test_predictions: pd.Series
) -> pd.DataFrame:
    """
    Create DataFrame with actual vs predicted values.
    
    Args:
        actual: Full actual time series
        train_predictions: Predictions on training set
        test_predictions: Predictions on test set
        
    Returns:
        DataFrame with columns: actual, predicted, residual
    """
    # Create combined predictions
    all_predictions = pd.concat([train_predictions, test_predictions])
    
    # Create DataFrame
    df = pd.DataFrame({
        "actual": actual,
        "predicted": all_predictions,
    })
    
    # Calculate residuals
    df["residual"] = df["actual"] - df["predicted"]
    
    return df
