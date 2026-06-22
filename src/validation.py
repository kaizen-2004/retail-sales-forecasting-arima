"""
Data validation module for quality checks.
"""

import pandas as pd
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a validation check."""
    passed: bool
    check_name: str
    message: str
    details: dict | None = None


def validate_date_gaps(df: pd.DataFrame, date_column: str = "Date", max_gap_days: int = 7) -> ValidationResult:
    """Check for large gaps in time series (expected for retail - stores closed some days)."""
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.sort_values(date_column).reset_index(drop=True)
    
    # Calculate gaps between consecutive dates
    df['date_diff'] = df[date_column].diff().dt.days
    large_gaps = df[df['date_diff'] > max_gap_days]
    
    passed = len(large_gaps) == 0
    return ValidationResult(
        passed=passed,
        check_name=f"No Gaps > {max_gap_days} Days",
        message=f"Found {len(large_gaps)} gaps larger than {max_gap_days} days" if not passed else f"No gaps larger than {max_gap_days} days",
        details={
            "gap_count": len(large_gaps),
            "max_gap": int(df['date_diff'].max()) if not df['date_diff'].isna().all() else 0,
            "missing_dates_total": len(pd.date_range(start=df[date_column].min(), end=df[date_column].max(), freq="D")) - len(df)
        }
    )


def validate_no_negative_values(df: pd.DataFrame, columns: list[str]) -> ValidationResult:
    """Check for negative values in specified columns."""
    issues = {}
    for col in columns:
        if col in df.columns:
            neg_count = (df[col] < 0).sum()
            if neg_count > 0:
                issues[col] = int(neg_count)
    
    passed = len(issues) == 0
    return ValidationResult(
        passed=passed,
        check_name="No Negative Values",
        message=f"Negative values found in: {list(issues.keys())}" if not passed else "No negative values",
        details=issues
    )


def validate_no_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> ValidationResult:
    """Check for duplicate rows."""
    dup_count = df.duplicated(subset=subset).sum()
    passed = dup_count == 0
    return ValidationResult(
        passed=passed,
        check_name="No Duplicates",
        message=f"Found {dup_count} duplicate rows" if not passed else "No duplicates",
        details={"duplicate_count": int(dup_count)}
    )


def validate_date_monotonic(df: pd.DataFrame, date_column: str = "Date") -> ValidationResult:
    """Check that dates are in chronological order."""
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])
    is_monotonic = df[date_column].is_monotonic_increasing
    return ValidationResult(
        passed=is_monotonic,
        check_name="Dates Monotonic",
        message="Dates are in order" if is_monotonic else "Dates are not in chronological order"
    )


def validate_min_records(df: pd.DataFrame, min_records: int) -> ValidationResult:
    """Check minimum number of records."""
    record_count = len(df)
    passed = record_count >= min_records
    return ValidationResult(
        passed=passed,
        check_name="Minimum Records",
        message=f"Found {record_count:,} records (min: {min_records:,})" if not passed else f"Sufficient records: {record_count:,}",
        details={"record_count": record_count, "min_required": min_records}
    )


def run_all_validations(df: pd.DataFrame, date_column: str = "Date") -> list[ValidationResult]:
    """
    Run all validation checks on the dataframe.
    
    Args:
        df: DataFrame to validate
        date_column: Name of the date column
        
    Returns:
        List of ValidationResult objects
    """
    results = [
        validate_date_gaps(df, date_column, max_gap_days=7),
        validate_date_monotonic(df, date_column),
        validate_no_duplicates(df, subset=[date_column]),
        validate_min_records(df, min_records=30),
    ]
    
    return results


def print_validation_report(results: list[ValidationResult]) -> None:
    """Print formatted validation report."""
    print("\n" + "="*60)
    print("DATA VALIDATION REPORT")
    print("="*60)
    
    all_passed = True
    for result in results:
        status = "✓ PASS" if result.passed else "✗ FAIL"
        print(f"\n{status}: {result.check_name}")
        print(f"  {result.message}")
        if result.details and not result.passed:
            for key, value in result.details.items():
                if isinstance(value, list) and len(value) > 5:
                    print(f"  {key}: {value[:5]}... ({len(value)} total)")
                else:
                    print(f"  {key}: {value}")
        if not result.passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL CHECKS PASSED")
    else:
        print("✗ SOME CHECKS FAILED - Review issues above")
    print("="*60 + "\n")
