import yfinance_procedures

DISCOUNT_RATE = 0.10 # in percentage (%)
GROWTH_RATE = 0.05 # in percentage (%)

# Define the ticker symbol
ticker_symbol = "IQ"

# Calculate Stock Intrinsic value per share
yfinance_procedures.calculate_intrinsic_value_per_share(ticker_symbol, r=DISCOUNT_RATE, g=GROWTH_RATE)