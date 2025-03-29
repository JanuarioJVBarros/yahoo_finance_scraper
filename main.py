import yfinance as yf

import yfinance_procedures

DISCOUNT_RATE = 0.10 # in percentage (%)
GROWTH_RATE = 0.05 # in percentage (%)

# Define the ticker symbol
ticker_symbol = "IQ"

# Create a Ticker object
ticker = yf.Ticker(ticker_symbol)

# Get current share value of a stock
yfinance_procedures.get_current_share_value(ticker)

# Calculate Stock Intrinsic value per share
yfinance_procedures.calculate_intrinsic_value_per_share(ticker, r=DISCOUNT_RATE, g=GROWTH_RATE)