from pathlib import Path
import pandas as pd


def load_cleaned_data(file_path):
    file_path = Path(file_path)
    df = pd.read_csv(file_path, parse_dates=["Order Date"])
    return df


def build_rfm(df, reference_date=None):
    if reference_date is None:
        reference_date = df["Order Date"].max() + pd.Timedelta(days=1)

    rfm = (
        df.groupby(["Customer ID", "Customer Name"], as_index=False)
        .agg(
            Recency=("Order Date", lambda x: (reference_date - x.max()).days),
            Frequency=("Order ID", "nunique"),
            Monetary=("Sales", "sum"),
        )
    )

    # Score customers on recency, frequency, and monetary value
    rfm["R_Score"] = pd.qcut(rfm["Recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)

    rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)

    def assign_segment(row):
        if row["R_Score"] >= 4 and row["F_Score"] >= 4 and row["M_Score"] >= 4:
            return "Champions"
        if row["R_Score"] >= 4 and row["F_Score"] >= 3:
            return "Loyal Customers"
        if row["F_Score"] >= 4 and row["M_Score"] >= 4:
            return "High Value"
        if row["R_Score"] <= 2 and row["F_Score"] <= 2:
            return "At Risk"
        return "Opportunity"

    rfm["Segment"] = rfm.apply(assign_segment, axis=1)
    return rfm


def save_rfm_scores(df, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    input_path = base_dir / "output" / "cleaned_sales.csv"
    output_path = base_dir / "output" / "rfm_scores.csv"

    print(f"Loading cleaned data from: {input_path}")
    df_cleaned = load_cleaned_data(input_path)
    print("Computing RFM scores...")
    df_rfm = build_rfm(df_cleaned)
    save_path = save_rfm_scores(df_rfm, output_path)
    print(f"RFM scores saved to: {save_path}")
