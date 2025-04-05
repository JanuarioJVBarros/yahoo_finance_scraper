# Intrinsic Value per Share Calculation
## Overview

This function calculates the **intrinsic value per share** of a stock using the **Discounted Cash Flow (DCF)** model, which is a widely used method to estimate the value of a company. The calculation uses the company's **Free Cash Flow (FCF)**, **Capital Expenditure (CapEx)**, **discount rate (r)**, and **growth rate (g)** over a forecast period.

## Formula

The **intrinsic value** of a stock is calculated as the sum of the present value (PV) of the forecasted Free Cash Flows (FCF) and the **present value of the terminal value (TV)**.

### Terminal Value Calculation (using the Gordon Growth Model):
```
$$TV = \frac{{FCF_{\text{n}} \times (1 + g)}}{{r - g}}$$

Where:
- \(FCF_{\text{n}}\) = Latest Free Cash Flow
- \(g\) = Growth rate (annual rate at which Free Cash Flow grows indefinitely)
- \(r\) = Discount rate (rate at which future cash flows are discounted)
```

### Present Value of Free Cash Flows (PV of FCFs):
```
$$PV_{\text{FCF}} = \sum_{t=1}^{n} \frac{{FCF_t}}{{(1 + r)^t}}$$

Where:
- \(FCF_t\) = Free Cash Flow for year \(t\)
- \(n\) = Forecast period (number of years of available Free Cash Flow)
```

### Intrinsic Value per Share:
```
$$\text{IV per Share} = \frac{{\text{PV}_{\text{FCF}} + \text{PV}_{\text{TV}}}}{{\text{Shares Outstanding}}}$$

Where:
- \( \text{Shares Outstanding} \) = Total number of shares outstanding for the company.
```

## Parameters

The function `calculate_intrinsic_value_per_share()` accepts the following parameters:

- **ticker (str or yfinance.Ticker)**: The stock ticker symbol (e.g., "AAPL" for Apple, "GOOGL" for Google) or a `yfinance.Ticker` object.
- **r (float)**: The **discount rate** (default is 0.08 or 8%).
- **g (float)**: The **growth rate** (default is 0.03 or 3%).

Both the discount rate (`r`) and growth rate (`g`) are expressed as decimal values (e.g., 8% as 0.08).

## Example Usage

```python
import yfinance as yf
import yfinance_procedures

# Get the Ticker object for Apple
ticker = yf.Ticker("AAPL")

# Calculate intrinsic value per share
intrinsic_value = yfinance_procedures.calculate_intrinsic_value_per_share(ticker, r=0.08, g=0.03)

# Print the result
print(f"Intrinsic Value per Share: {intrinsic_value}")
```

# Return on Equity (ROE) Calculation

## Description
The **Return on Equity (ROE)** is a financial ratio that measures the profitability of a company in relation to the equity held by its shareholders. It is calculated by dividing the company's **Net Income** by its **Shareholder's Equity** for a given year. The result is expressed as a percentage.

## Formula
The formula used to calculate ROE is:

```
ROE = (Net Income / Shareholder's Equity) * 100
```

Where:
- **Net Income** is the total profit earned by the company after expenses, taxes, and costs.
- **Shareholder's Equity** represents the value of a company's assets that shareholders own after liabilities are subtracted.

## Calculation Steps
1. **Extract Financial Data**: Retrieve the **Net Income** and **Shareholder's Equity** from the company's income statement and balance sheet, respectively.
2. **Remove NaN Values**: Drop any missing (NaN) values from both **Net Income** and **Shareholder's Equity** to ensure accurate calculations.
3. **Calculate ROE**: For each year, calculate the ROE as `Net Income / Shareholder's Equity` and multiply by 100 to convert it to a percentage.
4. **Return Results**: The ROE for each year is returned in a dictionary where the keys are the years and the values are the ROE percentages.

## Usage Example

```python
import yfinance as yf
import yfinance_procedures

# Get ticker symbol (e.g., AAPL)
ticker = yf.Ticker('AAPL')

# Calculate ROE
roe = yfinance_procedures.get_roe(ticker)

# Print ROE values for the years
print(roe)
```

# Debt-to-Equity Ratio Calculation

## Description
The **Debt-to-Equity Ratio** (D/E) is a financial ratio that compares a company's total debt to its shareholder equity. It is used to evaluate a company's financial leverage and how much debt the company is using to finance its operations relative to its equity. A high D/E ratio indicates that the company may be over-leveraged, while a low ratio suggests a more conservative financial structure.

## Formula
The formula used to calculate the Debt-to-Equity ratio is:

```
Debt-to-Equity Ratio = Total Debt / Shareholder's Equity
```

Where:
- **Total Debt** represents the sum of the company's liabilities, including both short-term and long-term debt.
- **Shareholder's Equity** is the net assets available to shareholders after liabilities have been deducted.

## Calculation Steps
1. **Extract Balance Sheet Data**: Retrieve the **Total Debt** and **Shareholder's Equity** from the company's balance sheet.
2. **Remove NaN Values**: Drop any missing (NaN) values from both **Total Debt** and **Shareholder's Equity** to ensure accurate calculations.
3. **Calculate Debt-to-Equity**: For each year, calculate the D/E ratio as `Total Debt / Shareholder's Equity`.
4. **Return Results**: The D/E ratio for each year is returned in a dictionary where the keys are the years and the values are the D/E ratios.

## Example Code
```python
import yfinance as yf
import yfinance_procedures

# Get ticker symbol (e.g., AAPL)
ticker = yf.Ticker('AAPL')

# Calculate Debt-to-Equity Ratio
debt_to_equity = yfinance_procedures.get_debt_to_equity(ticker)

# Print Debt-to-Equity ratios for the years
print(debt_to_equity)
```

# Profit Margins Calculation

## Description
The **Profit Margin** is a financial ratio that shows the percentage of revenue that remains as profit after all expenses are subtracted. It's an important indicator of a company's financial health, showing how efficiently a company is able to convert revenue into profits. There are various types of profit margins, but in this case, we are calculating the **Net Profit Margin**, which measures how much of each dollar of revenue is profit.

## Formula
The formula used to calculate **Net Profit Margin** is:

Net Profit Margin = (Net Income / Total Revenue) * 100


Where:
- **Net Income** is the company's total profit after all expenses have been deducted from total revenue.
- **Total Revenue** is the total amount of money the company has earned during a period from its business activities.

## Calculation Steps
1. **Extract Financial Data**: Retrieve the **Total Revenue** and **Net Income** from the company's income statement.
2. **Remove NaN Values**: Drop any missing (NaN) values from both **Total Revenue** and **Net Income** to ensure accurate calculations.
3. **Calculate Profit Margins**: For each year, calculate the Net Profit Margin as `(Net Income / Total Revenue) * 100`.
4. **Return Results**: The profit margins for each year are returned in a dictionary where the keys are the years and the values are the net profit margins.

## Usage Example

```python
import yfinance as yf
import yfinance_procedures

# Get ticker symbol (e.g., AAPL)
ticker = yf.Ticker('AAPL')

# Calculate Profit Margins
profit_margins = yfinance_procedures.get_profit_margins(ticker)

# Print Profit Margins for the years
print(profit_margins)
```

# Moat Analysis Calculation

## Description
A company's "moat" refers to its competitive advantage that allows it to maintain a sustainable market position over time. The following metrics are commonly used to assess a company's moat:

1. **Gross Margin**: A company with high and stable gross margins is often seen as having a strong moat, as it indicates pricing power and efficiency.
2. **Revenue Growth Rate**: Consistent revenue growth is another sign of a company with a strong competitive advantage.
3. **R&D as a Percentage of Revenue**: Companies investing heavily in research and development (R&D) may have a long-term competitive advantage due to innovation.

This function calculates these three metrics to help analyze a company's moat.

## Metrics Calculated
1. **Gross Margin**: Measures how much of each dollar of revenue is left over after subtracting the cost of goods sold (COGS).
    ```
    Gross Margin = (Gross Profit / Total Revenue) * 100
    ```

2. **Revenue Growth Rate**: Measures how the company's revenue is growing over time.
    ```
    Revenue Growth Rate = ((Revenue in Current Year - Revenue in Previous Year) / Revenue in Previous Year) * 100
    ```

3. **R&D as a Percentage of Revenue**: Measures the proportion of revenue spent on research and development.
    ```
    R&D as % of Revenue = (R&D Expenses / Total Revenue) * 100
    ```

## Calculation Steps
1. **Extract Financial Data**: Retrieve **Total Revenue**, **Gross Profit**, and **Research and Development** expenses from the company's financials.
2. **Calculate Gross Margin**: For each year, calculate **Gross Margin** as `(Gross Profit / Total Revenue) * 100`.
3. **Calculate Revenue Growth**: For each year, calculate the growth rate in revenue compared to the previous year.
4. **Calculate R&D as a Percentage of Revenue**: For each year, calculate the percentage of revenue spent on **Research and Development**.
5. **Return Results**: The function returns three dictionaries:
    - **Gross Margins** for each year.
    - **Revenue Growth** for each year.
    - **R&D as % of Revenue** for each year (if applicable).

## Usage Example

```python
import yfinance as yf
import yfinance_procedures

# Get ticker symbol (e.g., AAPL)
ticker = yf.Ticker('AAPL')

# Analyze Moat
gross_margins, revenue_growth, r_and_d_percent = yfinance_procedures.analyze_moat(ticker)

# Print results
print("Gross Margins:", gross_margins)
print("Revenue Growth:", revenue_growth)
print("R&D as % of Revenue:", r_and_d_percent)
```

# Management Evaluation Calculation

## Description
The evaluation of a company's management can be done by assessing two key aspects:

1. **Free Cash Flow (FCF)**: Free Cash Flow is a critical metric to understand how efficiently a company generates cash after spending money to maintain or expand its asset base. It's a measure of a company's ability to generate additional value.
2. **Insider Ownership**: The percentage of a company's shares owned by its insiders (e.g., executives, directors) can indicate the level of confidence the management has in the company's future.

This function calculates **Free Cash Flow** and retrieves **Insider Ownership** (if available) for a given ticker symbol.

## Metrics Calculated
1. **Free Cash Flow (FCF)**: Measures the cash available to investors after capital expenditures are deducted from operating cash flow.
    ```
    FCF = Operating Cash Flow - Capital Expenditures
    ```

2. **Insider Ownership**: The percentage of the company's stock owned by insiders (e.g., executives, directors).

## Calculation Steps
1. **Extract Financial Data**: Retrieve **Operating Cash Flow** and **Capital Expenditures** from the company's cash flow statement.
2. **Calculate Free Cash Flow (FCF)**: For each year, calculate **FCF** as `(Operating Cash Flow - Capital Expenditures)`.
3. **Retrieve Insider Ownership**: Fetch the percentage of shares held by company insiders, if available.
4. **Return Results**: The function returns two values:
    - A dictionary of **Free Cash Flow (FCF)** for each year.
    - The **Insider Ownership percentage** (if available).

## Usage Example

```python
import yfinance as yf
import yfinance_procedures

# Get ticker symbol (e.g., AAPL)
ticker = yf.Ticker('AAPL')

# Evaluate Management
free_cash_flow, insider_ownership = yfinance_procedures.evaluate_management(ticker)

# Print results
print("Free Cash Flow:", free_cash_flow)
print("Insider Ownership:", insider_ownership)
```

# PE Ratio Analysis

## Description
The **Price-to-Earnings (PE) Ratio** is a widely used metric to assess a company's valuation relative to its earnings. This method calculates two types of PE ratios:

1. **Trailing PE**: The PE ratio based on the company’s earnings over the past 12 months. It is calculated as:
   ```
   $$\text{Trailing PE} = \frac{\text{Current Price per Share}}{\text{Earnings per Share (EPS) over the past 12 months}}$$
   ```

2. **Forward PE**: The PE ratio based on forecasted earnings for the next 12 months. It is calculated as:
   ```
   $$\text{Forward PE} = \frac{\text{Current Price per Share}}{\text{Estimated EPS for the next 12 months}}$$
   ```

## Parameters
- `ticker`: The ticker symbol of the stock (using `yfinance` or `yahooquery`).

## Returns
- **trailing_pe**: The trailing PE ratio of the stock (or `'N/A'` if data is unavailable).
- **forward_pe**: The forward PE ratio of the stock (or `'N/A'` if data is unavailable).

## Usage example
```python
import yfinance as yf
import yfinance_procedures

# Get ticker symbol (e.g., AAPL)
ticker = yf.Ticker('AAPL')

# Example usage of the function:
trailing_pe, forward_pe = yfinance_procedures.get_pe_analysis(ticker)

print("Trailing PE:", trailing_pe)
print("Forward PE:", forward_pe)
```