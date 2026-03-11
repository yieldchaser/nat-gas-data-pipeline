import os
import yfinance as yf
import pandas as pd

def main():
    ticker = 'NG=F'
    start_date = '2015-01-01'
    
    print(f"Downloading {ticker} from {start_date} to today...")
    # Download historical data for NG=F
    df = yf.download(ticker, start=start_date)
    
    # Ensure Date becomes a column
    df = df.reset_index()
    
    # Flatten the dataframe if yfinance returns a multi-index header
    if isinstance(df.columns, pd.MultiIndex):
        print("Flattening multi-index columns...")
        df.columns = [col[0] for col in df.columns]
        
    # Isolate only the Date and Close columns
    if 'Date' not in df.columns or 'Close' not in df.columns:
        raise ValueError(f"Missing required columns. Available columns: {df.columns}")
        
    df = df[['Date', 'Close']]
    
    # Format the Date column strictly as DD-MM-YYYY (e.g., 11-03-2026)
    print("Formatting Date column as DD-MM-YYYY...")
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d-%m-%Y')
    
    # Drop rows with NaN in Close if any
    df = df.dropna(subset=['Close'])
    
    # Export the resulting dataframe to a CSV file without the index
    os.makedirs('data', exist_ok=True)
    out_path = 'data/nat_gas_continuous.csv'
    df.to_csv(out_path, index=False)
    print(f"Data successfully saved to {out_path}")

if __name__ == "__main__":
    main()
