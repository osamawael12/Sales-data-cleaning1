# Sales Data Cleaning

## Project Overview
This repository presents a professional end-to-end sales analytics workflow for cleaning, analyzing, and visualizing sales performance data. The project uses Python, Pandas, Jupyter, Matplotlib, Seaborn, and Plotly to transform raw sales records into business-ready insights.

## Tools Used
- Python 3.x
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly

## Project Structure
- `data/`: raw sales dataset files
- `notebooks/`: analysis and reporting notebooks
- `scripts/`: reusable Python modules for cleaning and RFM modeling
- `dashboard/`: interactive Plotly dashboard generator
- `output/`: cleaned data exports and generated output files

## Cleaning Steps
1. Load the raw sales dataset from `data/`
2. Remove duplicates and invalid rows
3. Handle missing values for key fields
4. Normalize numeric values and accounting formatting
5. Convert `Order Date` and `Ship Date` to datetime
6. Create engineered features: `Order Year`, `Order Month`, `Profit Margin`

## Key Performance Indicators
- Total Sales
- Total Profit
- Average Order Value
- Top Products by Sales
- Top Categories by Sales
- Monthly Sales Trend

## RFM Analysis
The project includes a second notebook for customer segmentation using:
- Recency: how recently customers purchased
- Frequency: how often customers place orders
- Monetary: total revenue by customer
- Customer segmentation for retention and loyalty planning

## Dashboard Overview
The Plotly dashboard generates interactive charts for:
- Top products
- Category sales share
- Monthly sales trend
- Profit by region

## How to Run
1. Create and activate your Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the data cleaning script:
   ```bash
   python scripts/clean_data.py
   ```
4. Run the RFM analysis script:
   ```bash
   python scripts/rfm_analysis.py
   ```
5. Generate the dashboard HTML:
   ```bash
   python dashboard/dashboard.py
   ```
6. Open the notebooks:
   - `notebooks/01_data_cleaning.ipynb`
   - `notebooks/02_rfm_analysis.ipynb`
