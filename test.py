import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Set the page config as the very first Streamlit command

st.set_page_config(layout="wide")
# Set the page title and layout
st.title('Real-Time Stock Price Analysis')


# Sidebar for selecting stock and date range
st.sidebar.header("Settings")
stock_symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")
start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=30))
end_date = st.sidebar.date_input("End Date", datetime.now())

# Fetch stock data
@st.cache
def load_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data

# Fetch data
data = load_data(stock_symbol, start_date, end_date)

# Display stock data
st.subheader(f'Stock Data for {stock_symbol}')
st.write(data.tail())

# Plot stock data using Plotly Express
fig = px.line(data, x=data.index, y='Close', title=f'{stock_symbol} Closing Prices', labels={'Close': 'Stock Price'})
st.plotly_chart(fig)

# Additional Stock Analysis (Moving Averages)
st.subheader('Moving Averages')
data['MA20'] = data['Close'].rolling(window=20).mean()  # 20-day moving average
data['MA50'] = data['Close'].rolling(window=50).mean()  # 50-day moving average

# Plot moving averages
fig_ma = px.line(data, x=data.index, y=['Close', 'MA20', 'MA50'], title=f'{stock_symbol} with Moving Averages', labels={'value': 'Stock Price', 'variable': 'Indicator'})
st.plotly_chart(fig_ma)

# Simple statistics
st.subheader('Stock Statistics')
st.write(f"Mean Closing Price: {np.mean(data['Close']):.2f}")
st.write(f"Standard Deviation of Closing Prices: {np.std(data['Close']):.2f}")
