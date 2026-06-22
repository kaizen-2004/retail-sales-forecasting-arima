"""
Automated pipeline for weekly sales forecasting.
"""

import logging
from pathlib import Path
from datetime import datetime
import pandas as pd

from src.data_processing import (
    load_excel_data,
    filter_valid_transactions,
    add_sales_column,
    aggregate_daily_sales,
)
from src.feature_engineering import create_forecast_features
from src.validation import run_all_validations, print_validation_report
from src.models import fit_sarima, calculate_metrics, train_test_split_time_series
from src.visualization import create_interactive_forecast, save_interactive_plot

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_pipeline(config: dict = None) -> dict:
    """
    Run the complete sales forecasting pipeline.
    
    Args:
        config: Configuration dictionary (uses defaults if None)
        
    Returns:
        Dictionary with pipeline results
    """
    if config is None:
        config = {
            "raw_data_path": "data/raw/Online Retail.xlsx",
            "processed_data_path": "data/processed",
            "reports_path": "reports",
            "model_order": (1, 1, 1),
            "seasonal_order": (1, 1, 1, 7),
            "test_size": 0.2,
        }
    
    results = {"status": "success", "steps": []}
    
    try:
        # Step 1: Load data
        logger.info("Step 1: Loading raw data...")
        raw_data_path = Path(config["raw_data_path"])
        if not raw_data_path.exists():
            raise FileNotFoundError(f"Raw data not found: {raw_data_path}")
        
        df_raw = load_excel_data(raw_data_path)
        logger.info(f"Loaded {len(df_raw):,} records")
        results["steps"].append({"step": "load_data", "status": "success", "records": len(df_raw)})
        
        # Step 2: Clean data
        logger.info("Step 2: Cleaning data...")
        df_clean = filter_valid_transactions(df_raw)
        df_clean = add_sales_column(df_clean)
        logger.info(f"Cleaned to {len(df_clean):,} records")
        results["steps"].append({"step": "clean_data", "status": "success", "records": len(df_clean)})
        
        # Step 3: Aggregate daily sales
        logger.info("Step 3: Aggregating daily sales...")
        daily_sales = aggregate_daily_sales(df_clean)
        logger.info(f"Aggregated to {len(daily_sales)} days")
        results["steps"].append({"step": "aggregate", "status": "success", "days": len(daily_sales)})
        
        # Step 4: Validate data
        logger.info("Step 4: Validating data quality...")
        validation_results = run_all_validations(daily_sales)
        print_validation_report(validation_results)
        all_passed = all(r.passed for r in validation_results)
        results["steps"].append({"step": "validate", "status": "success" if all_passed else "warning"})
        
        # Step 5: Create features
        logger.info("Step 5: Creating forecast features...")
        df_features = create_forecast_features(
            daily_sales,
            date_column='Date',
            target_column='total_sales',
            lags=[1, 7, 14, 28],
            windows=[7, 14, 28]
        )
        logger.info(f"Created {len(df_features.columns)} features")
        results["steps"].append({"step": "features", "status": "success", "features": len(df_features.columns)})
        
        # Step 6: Train model
        logger.info("Step 6: Training SARIMA model...")
        series = daily_sales.set_index('Date')['total_sales']
        train, test = train_test_split_time_series(series, test_size=config["test_size"])
        
        sarima_result = fit_sarima(
            train,
            order=config["model_order"],
            seasonal_order=config["seasonal_order"],
            forecast_steps=len(test)
        )
        
        metrics = calculate_metrics(test.values, sarima_result['predictions'].values)
        logger.info(f"Model trained - MAPE: {metrics['mape']:.2f}%")
        results["steps"].append({"step": "train_model", "status": "success", "mape": metrics['mape']})
        results["metrics"] = metrics
        
        # Step 7: Save outputs
        logger.info("Step 7: Saving outputs...")
        
        # Save processed data
        processed_path = Path(config["processed_data_path"])
        processed_path.mkdir(parents=True, exist_ok=True)
        daily_sales.to_csv(processed_path / "daily_sales_latest.csv", index=False)
        
        # Save forecast
        forecast_df = pd.DataFrame({
            'date': test.index,
            'actual': test.values,
            'predicted': sarima_result['predictions'].values,
        })
        forecast_df.to_csv(processed_path / "forecast_latest.csv", index=False)
        
        # Save interactive plot
        fig = create_interactive_forecast(
            actual=test,
            predicted=sarima_result['predictions'],
            title=f'Latest Forecast - {datetime.now().strftime("%Y-%m-%d")}'
        )
        reports_path = Path(config["reports_path"])
        save_interactive_plot(fig, f'forecast_{datetime.now().strftime("%Y%m%d")}', str(reports_path / "interactive"))
        
        logger.info("All outputs saved successfully")
        results["steps"].append({"step": "save_outputs", "status": "success"})
        
        # Step 8: Generate report
        logger.info("Step 8: Generating report...")
        report = generate_report(metrics, daily_sales, results)
        report_path = reports_path / "latest_report.txt"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(report)
        
        logger.info("Pipeline completed successfully!")
        results["steps"].append({"step": "generate_report", "status": "success"})
        results["report_path"] = str(report_path)
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        results["status"] = "failed"
        results["error"] = str(e)
        raise
    
    return results


def generate_report(metrics: dict, daily_sales: pd.DataFrame, results: dict) -> str:
    """
    Generate pipeline execution report.
    
    Args:
        metrics: Model metrics
        daily_sales: Daily sales DataFrame
        results: Pipeline results
        
    Returns:
        Report string
    """
    report = f"""
============================================================
PIPELINE EXECUTION REPORT
============================================================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: {results['status'].upper()}

DATA SUMMARY
------------
Total records processed: {results['steps'][0]['records']:,}
After cleaning: {results['steps'][1]['records']:,}
Daily aggregations: {results['steps'][2]['days']}
Date range: {daily_sales['Date'].min()} to {daily_sales['Date'].max()}
Total sales: £{daily_sales['total_sales'].sum():,.2f}

MODEL PERFORMANCE
-----------------
MAPE: {metrics['mape']:.2f}% (Target: ≤ 15%)
RMSE: £{metrics['rmse']:,.2f}
MAE: £{metrics['mae']:,.2f}
Status: {'✓ TARGET MET' if metrics['mape'] <= 15 else '✗ ABOVE TARGET'}

PIPELINE STEPS
--------------
"""
    for step in results["steps"]:
        status = "✓" if step["status"] == "success" else "⚠"
        report += f"{status} {step['step']}\n"
    
    report += f"""
OUTPUTS
-------
- Daily sales: data/processed/daily_sales_latest.csv
- Forecast: data/processed/forecast_latest.csv
- Interactive plot: reports/interactive/
- This report: reports/latest_report.txt

============================================================
"""
    return report


if __name__ == "__main__":
    logger.info("Starting sales forecasting pipeline...")
    results = run_pipeline()
    logger.info(f"Pipeline finished with status: {results['status']}")
