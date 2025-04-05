import argparse
from datetime import datetime
import openpyxl_procedures
import yfinance as yf
import yfinance_procedures

DISCOUNT_RATE = 0.10 # in percentage (%)
GROWTH_RATE = 0.05 # in percentage (%)

# Set up argument parsing
parser = argparse.ArgumentParser(description="Stock Ticker Script")

# Define required argument for tickers
parser.add_argument('tickers', nargs='+', help="List of stock ticker symbols (e.g., AAPL, GOOGL)")

# Parse the arguments
args = parser.parse_args()

# Access the tickers passed via the command line
print("Received tickers:", args.tickers)

header_list = ["Method", "Current Value", "Range", "Analysis"]
# Iterate over index and iterate over each stock
for ticker_symbol in args.tickers:
    # To store data resulting from the analysis
    row_list = []

    # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Get current share value of a stock
    current_share_value = yfinance_procedures.get_current_share_value(ticker)
    print(f"Current Share Value: ${current_share_value:.2f}")

    #############################
    ###    INTRINSIC VALUE    ###
    #############################
    # Calculate Stock Intrinsic value per share
    intrincic_share_value = yfinance_procedures.calculate_intrinsic_value_per_share(ticker, r=DISCOUNT_RATE, g=GROWTH_RATE)

    print("\n🔎 Intrinsic Value Analysis:")
    print(f"Intrinsic Value: ${intrincic_share_value:.2f}")

    if (intrincic_share_value - current_share_value) > 0:
        intrincic_share_analysis = "➡️ The stock appears to be **✅ UNDERVALUED**, meaning it may be a good buying opportunity based on intrinsic value."
    else:
        intrincic_share_analysis = "➡️ The stock appears to be **❌ OVERVALUED**, suggesting it may be trading at a price higher than its calculated intrinsic value."
    row_list.append(["Intrinsic Value", round(current_share_value, 2), intrincic_share_value, intrincic_share_analysis])

    #############################
    ###          ROE          ###
    #############################
    roe_data = yfinance_procedures.get_roe(ticker)
    print("\n🔎 Return on Equity (ROE) Analysis:")
    for year, roe in roe_data.items():
        status = "✅ Strong (Above 15%)" if roe > 15 else "⚠️ Below Ideal (Under 15%)"
        print(f"{year}: ROE = {roe:.2f}% {status}")
        row_list.append([f"Return on Equity (ROE)"])
        row_list.append([f"Return on Equity (ROE) {year}", round(roe, 2), "> 15%", status])

    #############################
    ###  Debt-to-Equity Ratio ###
    #############################
    debt_to_equity_data = yfinance_procedures.get_debt_to_equity(ticker)
    print("\n🔎 Debt-to-Equity Analysis:")
    for year, ratio in debt_to_equity_data.items():
        if ratio < 0.5:
            status = "✅ Low Debt (Safe Investment)"
        elif ratio <= 1.0:
            status = "⚠️ Moderate Debt (Caution Advised)"
        else:
            status = "❌ High Debt (Risky)"
        print(f"{year}: Debt-to-Equity = {ratio:.2f} {status}")
        row_list.append(["Debt-to-Equity"])
        row_list.append([f"Debt-to-Equity {year}", round(ratio, 2), "< 0,5", status])

    #############################
    ###     Profit Margins    ###
    #############################
    profit_margin_data = yfinance_procedures.get_profit_margins(ticker)
    print("\n🔎 Profit Margin Analysis:")
    for year, margin in profit_margin_data.items():
        status = "✅ Strong (>10%)" if margin > 10 else "⚠️ Weak (<10%)"
        print(f"{year}: Net Profit Margin = {margin:.2f}% {status}")
        row_list.append(["Profit Margin"])
        row_list.append([f"Profit Margin {year}", round(margin, 2), "> 10%", status])

    #############################
    ###          MOAT         ###
    #############################
    gross_margins, revenue_growth, r_and_d = yfinance_procedures.analyze_moat(ticker)
    print("\n🔎 Economic Moat Analysis:")
    print("🔹 Gross Margins:")
    if gross_margins is not None and revenue_growth is not None and r_and_d is not None:
        for year, margin in gross_margins.items():
            status = "✅ Strong (>40%)" if margin > 40 else "⚠️ Weak (<40%)"
            print(f"{year}: {margin:.2f}% {status}")
            row_list.append(["Gross Margin"])
            row_list.append([f"Gross Margin {year}", round(margin, 2), "> 40%", status])
        print("\n🔹 Revenue Growth:")
        for year, growth in revenue_growth.items():
            status = "✅ Growing (>5%)" if growth > 5 else "⚠️ Slow Growth (<5%)"
            print(f"{year}: {growth:.2f}% {status}")
            row_list.append(["Revenue Growth"])
            row_list.append([f"Revenue Growth {year}", round(growth, 2), "> 5%", status])
        if r_and_d:
            print("\n🔹 R&D Spending as % of Revenue:")
            for year, rd_percent in r_and_d.items():
                print(f"{year}: {rd_percent:.2f}%")
                row_list.append(["R&D Spending as % of Revenue"])
                row_list.append([f"R&D Spending as % of Revenue {year}", round(rd_percent, 2), "-", "-"])
    else:
        print(f"⚠️ Not enough data was retrieved to calculate Gross Margins!")


    #############################
    ###  Evaluate Management  ###
    #############################
    fcf_data, insider_ownership = yfinance_procedures.evaluate_management(ticker)
    print("\n🔎 Management Effectiveness Analysis:")
    print("🔹 Free Cash Flow (FCF):")
    for year, fcf in fcf_data.items():
        print(f"{year}: ${fcf:,.2f}")

    if insider_ownership is not None:
        status = "✅ High Insider Ownership (>10%)" if insider_ownership > 0.10 else "⚠️ Low Insider Ownership (<5%)"
        print(f"🔹 Insider Ownership: {insider_ownership * 100:.2f}% {status}")
    else:
        print("🔹 Insider Ownership Data is unavailable.")

    #############################
    ###   Price-per-Earning   ###
    #############################
    trailing_pe, forward_pe = yfinance_procedures.get_pe_analysis(ticker)
    print("\n🔎 PE Ratio Analysis:")
    print(f"🔹 Trailing PE Ratio: {trailing_pe}")
    print(f"🔹 Forward PE Ratio: {forward_pe}")
    if trailing_pe != 'N/A':
        if trailing_pe < 15:
            print("➡️ The trailing PE ratio is **below 15**, suggesting the stock is **✅ undervalued** relative to its past earnings.")
        elif 15 <= trailing_pe <= 25:
            print("➡️ The trailing PE ratio is **between 15 and 25**, indicating a **⚠️ fairly valued** stock.")
        else:
            print("➡️ The trailing PE ratio is **above 25**, which may suggest the stock is **❌ overvalued** unless strong growth is expected.")

    if forward_pe != 'N/A':
        if forward_pe < 15:
            print("➡️ The forward PE ratio is **below 15**, suggesting the stock **✅ may be undervalued** based on future earnings expectations.")
        elif 15 <= forward_pe <= 25:
            print("➡️ The forward PE ratio is **between 15 and 25**, indicating a **⚠️ fairly valued** stock given future earnings projections.")
        else:
            print("➡️ The forward PE ratio is **above 25**, suggesting the stock **❌ may be overvalued** unless future growth justifies the price.")

    openpyxl_procedures.write_to_excel(f"{ticker_symbol}_{datetime.now().strftime('%d_%m_%Y')}", header_list, row_list)
