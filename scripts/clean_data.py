from pathlib import Path
import pandas as pd


def load_data(file_path):
    """Load the raw sales dataset from a file path."""
    file_path = Path(file_path)
    return pd.read_csv(file_path, dtype=str)


def clean_numeric_column(series):
    """Normalize numeric strings and convert to numeric values."""
    cleaned = (
        series.astype(str)
        .str.strip()
        .str.replace(r"[\$,]", "", regex=True)
        .str.replace(r"\(", "-", regex=True)
        .str.replace(r"\)", "", regex=True)
        .str.replace("%", "", regex=False)
        .str.replace(r"\s+", "", regex=True)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def clean_data(df):
    """Perform end-to-end data cleaning on the sales dataset."""
    cleaned = df.copy(deep=True)

    cleaned.columns = cleaned.columns.str.strip()
    cleaned = cleaned.drop_duplicates(ignore_index=True)

    # Standardize text columns and fill known missing values
    for col in cleaned.select_dtypes(include=["object"]).columns:
        cleaned[col] = cleaned[col].astype(str).str.strip()

    if "Postal Code" in cleaned.columns:
        cleaned["Postal Code"] = cleaned["Postal Code"].replace({"nan": pd.NA})
        cleaned["Postal Code"] = cleaned["Postal Code"].fillna("Unknown")

    # Fix numeric columns stored as strings
    for col in ["Sales", "Profit", "Discount", "Sales Forecast"]:
        if col in cleaned.columns:
            cleaned[col] = clean_numeric_column(cleaned[col])

    # Convert date columns to datetime
    for date_col in ["Order Date", "Ship Date"]:
        if date_col in cleaned.columns:
            cleaned[date_col] = pd.to_datetime(cleaned[date_col], errors="coerce")

    # Drop rows missing essential business fields
    required_fields = ["Order ID", "Order Date", "Product ID", "Sales", "Profit"]
    required_fields = [col for col in required_fields if col in cleaned.columns]
    cleaned = cleaned.dropna(subset=required_fields).reset_index(drop=True)

    # Feature engineering
    if "Order Date" in cleaned.columns:
        cleaned["Order Year"] = cleaned["Order Date"].dt.year
        cleaned["Order Month"] = cleaned["Order Date"].dt.month

    if {"Profit", "Sales"}.issubset(cleaned.columns):
        cleaned["Profit Margin"] = cleaned.apply(
            lambda row: row["Profit"] / row["Sales"] if row["Sales"] != 0 else pd.NA,
            axis=1,
        )

    return cleaned


def save_cleaned_data(df, output_path):
    """Save the cleaned DataFrame to a CSV file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    raw_path = Path(__file__).resolve().parents[1] / "data" / "Sample - Superstore_Orders.csv"
    output_path = Path(__file__).resolve().parents[1] / "output" / "cleaned_sales.csv"

    print(f"Loading raw data from: {raw_path}")
    df_raw = load_data(raw_path)
    df_cleaned = clean_data(df_raw)

    print("Saving cleaned dataset...")
    saved_path = save_cleaned_data(df_cleaned, output_path)
    print(f"Cleaned dataset saved to: {saved_path}")
