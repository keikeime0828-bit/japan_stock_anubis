import time
import pandas as pd
from fetch_data_real import fetch_all_stocks
from anubis_learn import evaluate_stocks
from anubis_alert import send_slack_message

# ①②③候補銘柄
tickers = ["7203.T", "9984.T", "6758.T", "9433.T", "9983.T", "6861.T", "8035.T", "7974.T", "8306.T", "4063.T"]

def main():
    # 8:40: 初回通知
    df = fetch_all_stocks(tickers)
    # 仮でニュース/テクニカルスコア生成
    df['news_score'] = 1  # 実際はニュース評価
    df['technical_score'] = 2  # 実際はテクニカル評価

    df = evaluate_stocks(df)
    top10 = df.sort_values('score', ascending=False).head(10)
    
    send_slack_message("本日のトップ10銘柄評価:\n" + top10.to_string())

    # 取引中の10分ごとのシミュレーション
    for i in range(38):  # 8:50～15:00まで約10分毎
        time.sleep(600)  # 10分待機
        df = fetch_all_stocks(top10['ticker'].tolist())
        df['news_score'] = 1
        df['technical_score'] = 2
        df = evaluate_stocks(df)
        send_slack_message(f"{i+1}回目 10分ごとのシミュレーション:\n" + df.to_string())

    # 1日のまとめ
    send_slack_message("本日の取引まとめ:\n" + df.to_string())

if __name__ == "__main__":
    main()
