import os
import yfinance as yf
import pandas as pd


def compute_rolling_average(df, window=7, price_col='Close'):
    """Return a copy of df with a rolling average column added.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing at least the column specified by price_col.
    window : int
        Number of periods to include in the rolling window (default: 7).
    price_col : str
        Name of the column containing price values (default: 'Close').

    Returns
    -------
    pd.DataFrame
        Copy of df with a new column named f'{price_col}_MA{window}'.
    """
    if price_col not in df.columns:
        raise ValueError(f"Column '{price_col}' not found in DataFrame.")
    if window < 1:
        raise ValueError(f"Window must be a positive integer, got {window}.")

    result = df.copy()
    result[f'{price_col}_MA{window}'] = (
        result[price_col].rolling(window=window, min_periods=1).mean()
    )
    return result


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
