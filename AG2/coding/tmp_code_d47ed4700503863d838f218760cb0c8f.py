import matplotlib.pyplot as plt

# Replace the placeholders with the actual stock price data
meta_stock_prices_ytd = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
tesla_stock_prices_ytd = [200, 210, 220, 230, 240, 250, 260, 270, 280, 290]

# Create the plot
plt.plot(meta_stock_prices_ytd, label='META')
plt.plot(tesla_stock_prices_ytd, label='TESLA')

# Add labels and title
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.title('Stock Price Change YTD')

# Add legend
plt.legend()

# Save the plot as an image
plt.savefig('stock_price_ytd.png')

# Show the plot (optional)
# plt.show()