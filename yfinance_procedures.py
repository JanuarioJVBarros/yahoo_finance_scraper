import yfinance as yf

def calculate_intrinsic_value_per_share(ticker, r: float, g: float) -> float:
    # Access the 'info' attribute for company data
    company_info = ticker.info

    # Get the number of outstanding shares
    outstanding_shares = company_info.get('sharesOutstanding')
    if outstanding_shares is None:
        raise ValueError("Unable to retrieve sharesOutstanding.")

    # Fetch financial data
    cashflows = ticker.cashflow

    # Extract Free Cash Flow (FCF) and Capital Expenditure
    try:
        fcf_values = cashflows.loc["Free Cash Flow"] - cashflows.loc["Capital Expenditure"]
    except KeyError:
        raise ValueError("Missing 'Free Cash Flow' or 'Capital Expenditure' in the cashflow data.")
    
    fcf_values = fcf_values.sort_index(ascending=True)  # Sort in ascending order

    # It is possible that the fcf_values contain NaN values
    fcf_values = fcf_values.dropna()

    # Check if there are enough data points for the forecast period
    if len(fcf_values) < 1:
        raise ValueError("Not enough historical data to forecast.")

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

    return round(intrinsic_value_per_share, 2)

def get_current_share_value(ticker):
    return ticker.history(period="1d")["Close"].iloc[-1]

def get_roe(ticker):
    # Get financial data
    income_stmt = ticker.financials  # Net Income
    balance_sheet = ticker.balance_sheet  # Shareholder's Equity

    # Extract Net Income and Total Equity for the past years
    net_income = income_stmt.loc['Net Income']
    total_equity = balance_sheet.loc['Stockholders Equity']

    # It is possible that the total_equity contain NaN values
    total_equity = total_equity.dropna()

    # Calculate ROE for each year
    roe_values = {}
    for year in net_income.index:
        if year in total_equity and total_equity[year] != 0:
            roe = net_income[year] / total_equity[year]
            roe_values[year] = roe * 100  # Convert to percentage

    return roe_values

def get_debt_to_equity(ticker):
    # Get balance sheet data
    balance_sheet = ticker.balance_sheet

    # Extract Total Debt and Stockholders Equity
    try:
        total_debt = balance_sheet.loc['Total Debt']
        total_equity = balance_sheet.loc['Stockholders Equity']
    except KeyError:
        print("Some required financial data is missing.")
        return None

    # It is possible that the total_equity/total_debt contain NaN values
    total_equity = total_equity.dropna()
    total_debt = total_debt.dropna()

    # Calculate Debt-to-Equity ratio for each year
    debt_to_equity_ratios = {}
    for year in total_debt.index:
        if year in total_equity and total_equity[year] != 0:
            ratio = total_debt[year] / total_equity[year]
            debt_to_equity_ratios[year] = ratio

    return debt_to_equity_ratios

def get_profit_margins(ticker):
    # Get financial data
    income_stmt = ticker.financials  

    # Extract Revenue and Net Income
    try:
        revenue = income_stmt.loc['Total Revenue']
        net_income = income_stmt.loc['Net Income']
    except KeyError:
        print("Some required financial data is missing.")
        return None

    # It is possible that the revenue/net_income contain NaN values
    revenue = revenue.dropna()
    net_income = net_income.dropna()

    # Calculate Gross and Net Margins
    profit_margins = {}
    for year in revenue.index:
        if revenue[year] != 0:
            net_margin = (net_income[year] / revenue[year]) * 100  # Convert to %
            profit_margins[year] = net_margin

    return profit_margins

def analyze_moat(ticker):
    # Get financial data
    income_stmt = ticker.financials  

    # Extract Revenue, Gross Profit, and R&D Expenses
    try:
        revenue = income_stmt.loc['Total Revenue']
        gross_profit = income_stmt.loc['Gross Profit']
        r_and_d = income_stmt.loc['Research And Development']  # Some companies may not have this
    except KeyError:
        print("Some required financial data is missing.")
        return None, None, None

    # It is possible that the revenue/gross_profit/r_and_d contain NaN values
    revenue = revenue.dropna()
    gross_profit = gross_profit.dropna()
    r_and_d = r_and_d.dropna()

    # Calculate Gross Margin %
    gross_margins = {}
    for year in revenue.index:
        if revenue[year] != 0:
            gross_margin = (gross_profit[year] / revenue[year]) * 100
            gross_margins[year] = gross_margin

    # Calculate Revenue Growth Rate
    revenue_growth = {}
    previous_year = None
    for year in sorted(revenue.index, reverse=True):
        if previous_year:
            growth_rate = ((revenue[year] - revenue[previous_year]) / revenue[previous_year]) * 100
            revenue_growth[year] = growth_rate
        previous_year = year

    # Calculate R&D as % of Revenue (if applicable)
    r_and_d_percent = {}
    if r_and_d is not None:
        for year in revenue.index:
            if revenue[year] != 0 and year in r_and_d:
                r_and_d_percent[year] = (r_and_d[year] / revenue[year]) * 100

    return gross_margins, revenue_growth, r_and_d_percent

def evaluate_management(ticker):
    # Get financial data
    cashflow_stmt = ticker.cashflow

    # Extract Free Cash Flow (FCF)
    try:
        operating_cash_flow = cashflow_stmt.loc['Operating Cash Flow']
        capital_expenditures = cashflow_stmt.loc['Capital Expenditure']
    except KeyError:
        print("Some required financial data is missing.")
        return None
    
    # It is possible that the operating_cash_flow/gross_profit/r_and_d contain NaN values
    operating_cash_flow = operating_cash_flow.dropna()
    capital_expenditures = capital_expenditures.dropna()

    # Calculate Free Cash Flow (FCF)
    free_cash_flow = {}
    for year in operating_cash_flow.index:
        fcf = operating_cash_flow[year] - capital_expenditures[year]
        free_cash_flow[year] = fcf

    # Extract Insider Ownership (if available)
    try:
        insider_ownership = ticker.info['heldPercentInsiders']
    except KeyError:
        print("Insider ownership data is missing.")
        insider_ownership = None
    
    return free_cash_flow, insider_ownership

def get_pe_analysis(ticker):
    # Get PE Ratios (Trailing and Forward)
    trailing_pe = ticker.info.get('trailingPE', 'N/A')
    forward_pe = ticker.info.get('forwardPE', 'N/A')

    return trailing_pe, forward_pe