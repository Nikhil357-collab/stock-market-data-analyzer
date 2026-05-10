from src.data_loader import fetch_stock_data
from src.cleaner import clean_data
from src.indicators import add_indicators
from src.analysis import analyze_stock
from src.visualisation import create_visualizations
from src.report_generator import generate_report

# USER INPUT
ticker = "AAPL"
start_date = "2023-01-01"
end_date = "2024-01-01"

# STEP 1: LOAD DATA
df = fetch_stock_data(ticker, start_date, end_date)

# STEP 2: CLEAN DATA
df = clean_data(df)

# STEP 3: CALCULATE INDICATORS
df = add_indicators(df)

# STEP 4: ANALYSIS
summary = analyze_stock(df)

# STEP 5: VISUALIZATION
create_visualizations(df, ticker)

# STEP 6: REPORT GENERATION
generate_report(summary, ticker)

print("\nProject Execution Completed Successfully!")