"""Financial Performance Dashboard.

Run with: streamlit run app.py
Add more companies by adding rows to the two CSV files in data/.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Financial Performance Dashboard", page_icon="📈", layout="wide")

DATA_FOLDER = Path(__file__).parent / "data"


@st.cache_data
def load_data():
    """Read the project data files once, then reuse them while the app is open."""
    financials = pd.read_csv(DATA_FOLDER / "company_financials.csv")
    prices = pd.read_csv(DATA_FOLDER / "stock_prices.csv", parse_dates=["date"])
    return financials, prices


def dollars(value, decimals=0):
    """Format a number as dollars for cards and charts."""
    return f"${value:,.{decimals}f}"


financials, prices = load_data()
companies = sorted(financials["company"].unique())

st.title("Financial Performance Dashboard")
st.caption("Annual financials in USD millions | Monthly stock prices use adjusted close")

selected_company = st.sidebar.selectbox("Choose a company", companies)
company_financials = financials[financials["company"] == selected_company].sort_values("fiscal_year")
company_prices = prices[prices["company"] == selected_company].sort_values("date")

st.sidebar.markdown("---")
st.sidebar.info("To add another company, add matching company rows to both CSV files in the data folder.")

latest = company_financials.iloc[-1]
previous = company_financials.iloc[-2]
revenue_growth = (latest["revenue_millions"] / previous["revenue_millions"] - 1) * 100
income_growth = (latest["net_income_millions"] / previous["net_income_millions"] - 1) * 100
free_cash_flow = latest["operating_cash_flow_millions"] - latest["capital_expenditures_millions"]

st.subheader(f"{selected_company}: {int(latest['fiscal_year'])} at a glance")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Revenue", dollars(latest["revenue_millions"]), f"{revenue_growth:.1f}% vs. prior year")
col2.metric("Net income", dollars(latest["net_income_millions"]), f"{income_growth:.1f}% vs. prior year")
col3.metric("Diluted EPS", dollars(latest["diluted_eps"], 2))
col4.metric("Free cash flow", dollars(free_cash_flow))

st.divider()

left, right = st.columns(2)
with left:
    st.subheader("Revenue and net income")
    income_chart_data = company_financials.melt(
        id_vars="fiscal_year",
        value_vars=["revenue_millions", "net_income_millions"],
        var_name="Metric",
        value_name="USD millions",
    )
    income_chart_data["Metric"] = income_chart_data["Metric"].map(
        {"revenue_millions": "Revenue", "net_income_millions": "Net income"}
    )
    fig = px.bar(income_chart_data, x="fiscal_year", y="USD millions", color="Metric", barmode="group")
    fig.update_layout(xaxis_title="Fiscal year", legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Profit margins")
    margins = pd.DataFrame(
        {
            "Fiscal year": company_financials["fiscal_year"],
            "Gross margin": company_financials["gross_profit_millions"] / company_financials["revenue_millions"] * 100,
            "Operating margin": company_financials["operating_income_millions"] / company_financials["revenue_millions"] * 100,
            "Net margin": company_financials["net_income_millions"] / company_financials["revenue_millions"] * 100,
        }
    ).melt(id_vars="Fiscal year", var_name="Margin", value_name="Percent")
    fig = px.line(margins, x="Fiscal year", y="Percent", color="Margin", markers=True)
    fig.update_layout(yaxis_ticksuffix="%", xaxis_title="Fiscal year", legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Cash flow")
    cash_flow = pd.DataFrame(
        {
            "Fiscal year": company_financials["fiscal_year"],
            "Operating cash flow": company_financials["operating_cash_flow_millions"],
            "Capital expenditures": -company_financials["capital_expenditures_millions"],
            "Free cash flow": company_financials["operating_cash_flow_millions"]
            - company_financials["capital_expenditures_millions"],
        }
    ).melt(id_vars="Fiscal year", var_name="Metric", value_name="USD millions")
    fig = px.bar(cash_flow, x="Fiscal year", y="USD millions", color="Metric", barmode="group")
    fig.update_layout(xaxis_title="Fiscal year", legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Cash and total debt")
    balance = company_financials.melt(
        id_vars="fiscal_year",
        value_vars=["cash_and_equivalents_millions", "total_debt_millions"],
        var_name="Metric",
        value_name="USD millions",
    )
    balance["Metric"] = balance["Metric"].map(
        {"cash_and_equivalents_millions": "Cash and equivalents", "total_debt_millions": "Total debt"}
    )
    fig = px.bar(balance, x="fiscal_year", y="USD millions", color="Metric", barmode="group")
    fig.update_layout(xaxis_title="Fiscal year", legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Stock-price performance")
first_price = company_prices.iloc[0]["adjusted_close"]
last_price = company_prices.iloc[-1]["adjusted_close"]
stock_return = (last_price / first_price - 1) * 100
st.caption(
    f"Adjusted close: {dollars(first_price, 2)} on {company_prices.iloc[0]['date']:%b %d, %Y} "
    f"to {dollars(last_price, 2)} on {company_prices.iloc[-1]['date']:%b %d, %Y} ({stock_return:.1f}%)."
)
fig = px.line(company_prices, x="date", y="adjusted_close", markers=True)
fig.update_layout(xaxis_title="Month", yaxis_title="Adjusted close (USD)")
fig.update_traces(line_color="#1f77b4")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Key Insights")
gross_margin = latest["gross_profit_millions"] / latest["revenue_millions"] * 100
net_margin = latest["net_income_millions"] / latest["revenue_millions"] * 100
debt_change = (latest["total_debt_millions"] / company_financials.iloc[0]["total_debt_millions"] - 1) * 100

st.markdown(
    f"""
- **Growth:** Revenue changed from {dollars(company_financials.iloc[0]['revenue_millions'])} in fiscal {int(company_financials.iloc[0]['fiscal_year'])} to {dollars(latest['revenue_millions'])} in fiscal {int(latest['fiscal_year'])}; the latest annual growth rate was **{revenue_growth:.1f}%**.
- **Profitability:** In fiscal {int(latest['fiscal_year'])}, {selected_company} earned a **{gross_margin:.1f}% gross margin** and **{net_margin:.1f}% net margin**.
- **Cash generation:** Latest free cash flow was **{dollars(free_cash_flow)}**, after spending {dollars(latest['capital_expenditures_millions'])} on capital expenditures.
- **Capital structure:** Total debt changed **{debt_change:.1f}%** across the displayed period and ended at **{dollars(latest['total_debt_millions'])}**.
- **Stock performance:** The adjusted share price changed **{stock_return:.1f}%** over the monthly price period shown.
"""
)

with st.expander("View annual source data"):
    display_data = company_financials.copy()
    display_data.columns = [column.replace("_", " ").title() for column in display_data.columns]
    st.dataframe(display_data, use_container_width=True, hide_index=True)
