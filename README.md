# Natural Gas Data Pipeline

A fully automated data pipeline designed to pull continuous front-month natural gas futures data (`NG=F`) daily from Yahoo Finance, format it specifically for downstream Excel models, and push the updated dataset to this repository using GitHub Actions.

## 🚀 Overview

This repository automates the retrieval of natural gas futures prices, replacing broken Excel `STOCKHISTORY` functions. 

The python script fetches historical data starting from `2015-01-01` to the current date and isolates the `Date` and `Close` columns. Crucially, it formats the `Date` column strictly as `DD-MM-YYYY` to ensure compatibility with existing Excel models. 

## 📂 Repository Structure

```
├── .github/workflows/
│   └── daily_update.yml       # GitHub Actions pipeline configuration
├── data/
│   ├── .gitkeep               # Ensures the empty data folder is tracked
│   └── nat_gas_continuous.csv # The generated dataset (updated daily)
├── scripts/
│   └── update_ng_prices.py    # Python script that fetches and formats the data
├── .gitignore
├── README.md                  # This file
└── requirements.txt           # Python dependencies (yfinance, pandas)
```

## ⚙️ Automation (GitHub Actions)

The pipeline is fully automated via GitHub Actions (`.github/workflows/daily_update.yml`).

- **Schedule:** Runs automatically at `23:00 UTC`, Monday through Friday (`0 23 * * 1-5`).
- **Manual Trigger:** Can be manually triggered at any time using the `workflow_dispatch` event from the Actions tab in GitHub.
- **Environment:** Runs on `ubuntu-latest` using `Python 3.10`. Environment variables are configured to automatically force Javascript actions to `Node 24` to avoid deprecation warnings.
- **Workflow:** 
  1. Checks out the repository.
  2. Sets up Python and installs required dependencies (`yfinance`, `pandas`).
  3. Executes `scripts/update_ng_prices.py`.
  4. Automatically commits and pushes the updated `data/nat_gas_continuous.csv` using the `github-actions[bot]` identity, but **only if new data changes are detected**.

## 🛠️ Local Development

To run the script locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/yieldchaser/nat-gas-data-pipeline.git
   cd nat-gas-data-pipeline
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Python script:
   ```bash
   python scripts/update_ng_prices.py
   ```
   
The updated dataset will be saved at `data/nat_gas_continuous.csv`.