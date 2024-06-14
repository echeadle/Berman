# filename: stock_comparison.py

import yfinance as yf
from datetime import datetime

# Get the current date
current_date = datetime.now().strftime('%Y-%m-%d')
print(f"Current Date: {current_date}")

# Define the stock symbols
stocks = ['META', 'TSLA']

# Get the stock data for the beginning of the year and the current date
start_date = f"{datetime.now().year}-01-01"

# Fetch stock data
data = yf.download(stocks, start=start_date, end=current_date)

# Get the opening prices at the start of the year and the latest closing prices
start_prices = data['Open'].iloc[0]
current_prices = data['Close'].iloc[-1]

# Calculate the year-to-date gain
gains = ((current_prices - start_prices) / start_prices) * 100

# Print the results
print(f"Year-to-date gain for META: {gains['META']:.2f}%")
print(f"Year-to-date gain for TESLA: {gains['TSLA']:.2f}%")

# Compare the gains
if gains['META'] > gains['TSLA']:
    print("META has a higher year-to-date gain than TESLA.")
elif gains['META'] < gains['TSLA']:
    print("TESLA has a higher year-to-date gain than META.")
else:
    print("META and TESLA have the same year-to-date gain.")