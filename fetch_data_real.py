import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker):
    hist = yf.Ticker(ticker).history(period="2d")

    current_price = hist['Close'].iloc[-1]
    prev_close    = hist['Close'].iloc[-2]
    volume_change = int(hist['Volume'].iloc[-1] / (hist['Volume'].iloc[-2] + 1e-5) * 100 - 100)

    return {
        "ticker": ticker,
        "current_price": current_price,
        "prev_close": prev_close,
        "volume_change": volume_change
    }

def fetch_all_stocks(tickers):
    data = []
    for t in tickers:
        data.append(fetch_stock_data(t))
    return pd.DataFrame(data)
