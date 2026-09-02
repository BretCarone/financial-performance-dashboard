# Financial Performance Dashboard

A beginner-friendly Streamlit dashboard for comparing a company's annual financial performance and monthly adjusted stock-price data.

## What this project shows

- Revenue, net income, and diluted EPS
- Gross, operating, and net profit margins
- Operating cash flow, capital expenditures, and free cash flow
- Cash and total debt
- Monthly adjusted stock-price performance
- Automatically calculated Key Insights

The included data is Apple, Microsoft, and NVIDIA fiscal 2023-2025. All financial statement values are in USD millions.

## Run it on Windows

### 1. Install Python

1. Go to https://www.python.org/downloads/windows/.
2. Download the current Python 3 installer.
3. Open the installer.
4. **Before clicking Install Now, check the box called `Add python.exe to PATH`.**
5. Click **Install Now**, then finish the installation.

### 2. Open the project folder

1. Download and unzip this project folder somewhere easy to find, such as your Desktop.
2. Open the folder in File Explorer.
3. Click the address bar, type `cmd`, and press Enter. A black Command Prompt window will open in the correct folder.

### 3. Create a project environment

Copy and paste these commands, one at a time:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the dashboard

```bat
streamlit run app.py
```

Your browser should open to `http://localhost:8501` automatically. Leave the Command Prompt open while you use the dashboard. To stop it later, click the Command Prompt and press `Ctrl` + `C`.

## Add another company

The company dropdown is created from the `company` column in the two files inside `data`.

1. Add three annual rows for the new company to `data/company_financials.csv`.
2. Add monthly adjusted-close rows for the same company to `data/stock_prices.csv`.
3. Use exactly the same company name in both files. For example, use `Microsoft` in every Microsoft row.
4. Save the files. Streamlit will refresh the dashboard automatically.

### Annual financial-data columns

```text
company, fiscal_year, revenue_millions, gross_profit_millions,
operating_income_millions, net_income_millions, diluted_eps,
operating_cash_flow_millions, capital_expenditures_millions,
cash_and_equivalents_millions, total_debt_millions
```

Total debt should equal commercial paper plus current term debt plus non-current term debt when those categories exist.

### Stock-price-data columns

```text
company, date, adjusted_close
```

Use dates written as `YYYY-MM-DD`, such as `2025-09-30`.

## Resume-ready description

Built a Python financial performance dashboard using Streamlit, pandas, and Plotly to visualize multi-year revenue, profitability, cash flow, capital structure, and adjusted stock-price performance. Designed a reusable CSV-based data model supporting comparison across companies.

## Data sources

Annual financial figures for Apple, Microsoft, and NVIDIA were transcribed from company Form 10-K filings. Included monthly stock-price values use adjusted close.
