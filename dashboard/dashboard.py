from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def load_data(file_path):
    return pd.read_csv(file_path, parse_dates=["Order Date"])


def create_dashboard(df, output_path):
    top_products = df.groupby("Product Name", as_index=False)["Sales"].sum().nlargest(10, "Sales")
    category_sales = df.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    monthly_sales = (
        df.groupby([df["Order Date"].dt.to_period("M")])["Sales"]
        .sum()
        .reset_index()
        .assign(Order_Month=lambda x: x["Order Date"].dt.to_timestamp())
    )
    region_profit = df.groupby("Region", as_index=False)["Profit"].sum().sort_values("Profit", ascending=False)

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=[
            "Top 10 Products by Sales",
            "Sales by Category",
            "Monthly Sales Trend",
            "Profit by Region",
        ],
        specs=[[{"type": "bar"}, {"type": "pie"}], [{"type": "scatter"}, {"type": "bar"}]],
    )

    fig.add_trace(
        go.Bar(x=top_products["Sales"], y=top_products["Product Name"], orientation="h", marker_color="#2a9d8f", name="Top Products"),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Pie(labels=category_sales["Category"], values=category_sales["Sales"], hole=0.4, name="Category Sales"),
        row=1,
        col=2,
    )

    fig.add_trace(
        go.Scatter(x=monthly_sales["Order_Month"], y=monthly_sales["Sales"], mode="lines+markers", marker=dict(color="#264653"), name="Monthly Sales"),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Bar(x=region_profit["Region"], y=region_profit["Profit"], marker_color="#e76f51", name="Profit by Region"),
        row=2,
        col=2,
    )

    fig.update_layout(
        title_text="Sales Analysis Dashboard",
        height=900,
        showlegend=False,
        template="plotly_white",
    )
    fig.update_xaxes(tickangle=-45)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_path, include_plotlyjs="cdn")
    return output_path


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    input_path = base_dir / "output" / "cleaned_sales.csv"
    dashboard_path = base_dir / "output" / "sales_dashboard.html"

    print(f"Loading cleaned dataset from: {input_path}")
    df = load_data(input_path)
    dashboard_file = create_dashboard(df, dashboard_path)
    print(f"Dashboard saved to: {dashboard_file}")
