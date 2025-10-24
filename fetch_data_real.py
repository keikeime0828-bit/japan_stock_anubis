import yfinance as yf
import pandas as pd
import random

def fetch_market_news(tickers):
    """ニュース・材料によるスコアを反映（簡易版）"""
    news_score = {}
    for t in tickers:
        score = random.choice([0,1,2])
        news_score[t] = score
    return news_score

def build_combined_data(tickers):
    """最新株価・出来高・急騰アラート・ニューススコアをまとめたDataFrame"""
    news_score = fetch_market_news(tickers)
    data = []

    for t in tickers:
        yf_ticker = t.replace(".T",".T")  # yfinance形式
        stock = yf.Ticker(yf_ticker)
        hist = stock.history(period="2d")
        if len(hist) < 2:
            current_price = 0
            prev_close = 0
        else:
            current_price = hist['Close'][-1]
            prev_close = hist['Close'][-2]
        diff_pct = round((current_price - prev_close)/prev_close*100,2)
        volume_change = int(hist['Volume'][-1] / (hist['Volume'][-2] + 1e-5) * 100 - 100)
        alerts = "株価急騰" if diff_pct > 1 else ""
        data.append({
            "ticker": t,
            "current_price": current_price,
            "prev_close": prev_close,
            "diff_pct": diff_pct,
            "volume_change": volume_change,
            "news_score": news_score[t],
            "alerts": alerts
        })
    return pd.DataFrame(data)
