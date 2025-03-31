import yahooquery as yq
from yahooquery import Ticker

# Function to get a list of stocks of an index
def get_index_stocks(index_symbol):
    # Use SPY ETF (S&P 500 tracker)
    index_ticker = Ticker(index_symbol)

    # Fetch fund top holdings
    holdings_data = index_ticker.fund_top_holdings
    print(holdings_data)
    # Check if data exists
    if "SPY" in holdings_data and "holdings" in holdings_data["SPY"]:
        sp500_stocks = [stock["symbol"] for stock in holdings_data["SPY"]["holdings"]]
        return sp500_stocks
    else:
        print("No holdings data found.")
        return []
