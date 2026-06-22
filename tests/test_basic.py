"""
Basic tests for the Sales Forecasting project.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_processing import (
    load_excel_data,
    get_data_info,
    filter_valid_transactions,
    add_sales_column,
    aggregate_daily_sales,
)
from src.utils import get_project_root, ensure_directories


class TestUtils:
    """Test utility functions."""
    
    def test_get_project_root(self):
        """Test project root path."""
        root = get_project_root()
        assert root.exists()
        assert (root / "src").exists()
    
    def test_ensure_directories(self):
        """Test directory creation."""
        ensure_directories()
        root = get_project_root()
        assert (root / "data" / "raw").exists()
        assert (root / "data" / "processed").exists()
        assert (root / "data" / "database").exists()


class TestDataProcessing:
    """Test data processing functions."""
    
    @pytest.fixture
    def sample_df(self):
        """Create sample transaction data."""
        return pd.DataFrame({
            "InvoiceNo": ["12345", "12346", "C12347", "12348", "12349"],
            "StockCode": ["ABC", "DEF", "GHI", "JKL", "MNO"],
            "Description": ["Product A", "Product B", "Product C", "Product D", "Product E"],
            "Quantity": [10, 5, -3, 8, 2],
            "InvoiceDate": pd.to_datetime(["2010-12-01", "2010-12-02", "2010-12-03", "2010-12-04", "2010-12-05"]),
            "UnitPrice": [10.0, 20.0, 15.0, 0.5, 100.0],
            "CustomerID": [12345.0, 12346.0, np.nan, 12348.0, 12349.0],
            "Country": ["UK", "UK", "UK", "UK", "UK"],
        })
    
    def test_get_data_info(self, sample_df):
        """Test data info extraction."""
        info = get_data_info(sample_df)
        assert info["shape"] == (5, 8)
        assert "InvoiceNo" in info["columns"]
        assert info["missing_values"]["CustomerID"] == 1
    
    def test_filter_valid_transactions(self, sample_df):
        """Test transaction filtering."""
        filtered = filter_valid_transactions(sample_df)
        # Should remove: C12347 (cancelled), row with NaN CustomerID, negative quantity
        assert len(filtered) == 2
        assert "C" not in filtered["InvoiceNo"].astype(str).values
    
    def test_add_sales_column(self, sample_df):
        """Test sales column creation."""
        df_with_sales = add_sales_column(sample_df)
        assert "Sales" in df_with_sales.columns
        assert df_with_sales["Sales"].iloc[0] == 100.0  # 10 * 10.0
    
    def test_aggregate_daily_sales(self, sample_df):
        """Test daily sales aggregation."""
        df_with_sales = add_sales_column(sample_df)
        # Filter first to have valid data
        df_filtered = filter_valid_transactions(sample_df)
        df_filtered = add_sales_column(df_filtered)
        
        daily = aggregate_daily_sales(df_filtered)
        assert "total_sales" in daily.columns
        assert "transaction_count" in daily.columns
        assert len(daily) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
