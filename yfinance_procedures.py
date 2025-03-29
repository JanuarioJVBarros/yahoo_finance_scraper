import yfinance as yf

def calculate_intrinsic_value_per_share(ticker_symbol: str, r: float, g: float) -> float: 
    # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Access the 'info' attribute for company data
    company_info = ticker.info

    # Get the number of outstanding shares
    outstanding_shares = company_info.get('sharesOutstanding')

    # Fetch financial data
    cashflows = ticker.cashflow

    # Extract Free Cash Flow (FCF)
    fcf_values = cashflows.loc["Free Cash Flow"] - cashflows.loc["Capital Expenditure"]
    fcf_values = fcf_values.sort_index(ascending=True)  # Sort in ascending order

    # It is possible that the fcf_values contain NaN values
    fcf_values = fcf_values.dropna()

    n = len(fcf_values)  # Forecast period (years)
    latest_fcf = fcf_values.iloc[-1]  # Most recent Free Cash Flow

    # Terminal Value (TV) using Gordon Growth Model
    tv = (latest_fcf * (1 + g)) / (r - g)

    # Present Value of Terminal Value
    tv_pv = tv / ((1 + r) ** n)

    # Present Value of Free Cash Flows (Discounting Each Year's FCF)
    pv_fcfs = sum(fcf_values.iloc[i] / ((1 + r) ** (i + 1)) for i in range(n))

    # Intrinsic Value Calculation
    intrinsic_value = pv_fcfs + tv_pv

    # Split the total Intrinsic Value per Outstanding Shares
    intrinsic_value_per_share = intrinsic_value / outstanding_shares

    print(f"Intrinsic Value of {ticker_symbol}: ${intrinsic_value_per_share:.2f}")

    return intrinsic_value_per_share
