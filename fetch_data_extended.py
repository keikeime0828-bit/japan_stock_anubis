import pandas as pd
import random

def fetch_market_news(tickers):
    """ニュース・材料によるスコアを簡易反映"""
    news_score = {}
    for t in tickers:
        score = random.choice([0,1,2])  # 0:特になし, 1:好材料, 2:超好材料
        news_score[t] = score
    return news_score

def build_combined_data(tickers):
    """最新株価・出来高・急騰アラート・ニューススコアをまとめたDataFrame"""
    news_score = fetch_market_news(tickers)
    data = []
    for t in tickers:
        current_price = 1000 + random.randint(-10, 10)
        volume_change = random.randint(5,20)
        diff_pct = round((current_price - 1000)/1000*100,2)
        alerts = "株価急騰" if diff_pct > 1 else ""
        data.append({
            "ticker": t,
            "current_price": current_price,
            "volume_change": volume_change,
            "diff_pct": diff_pct,
            "news_score": news_score[t],
            "alerts": alerts
        })
    return pd.DataFrame(data)
