"""
Utility functions for the Sales Forecasting project.
"""

import os
from pathlib import Path


def get_project_root() -> Path:
    """Get the root directory of the project."""
    return Path(__file__).parent.parent


def get_data_dir() -> Path:
    """Get the data directory path."""
    return get_project_root() / "data"


def get_raw_data_dir() -> Path:
    """Get the raw data directory path."""
    return get_data_dir() / "raw"


def get_processed_data_dir() -> Path:
    """Get the processed data directory path."""
    return get_data_dir() / "processed"


def get_database_dir() -> Path:
    """Get the database directory path."""
    return get_data_dir() / "database"


def ensure_directories():
    """Ensure all required directories exist."""
    directories = [
        get_raw_data_dir(),
        get_processed_data_dir(),
        get_database_dir(),
        get_project_root() / "reports" / "figures",
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
