import datetime
import os
import time
import pandas as pd
from fetch_data_real import build_combined_data
from fetch_board_news import fetch_board_info, fetch_latest_news
from anubis_alert import send_alert
from anubis_learn import get_top_predictions, evaluate_stocks

TICKERS = ["7203.T","6758.T","9984.T","9432.T","8035.T","6098.T","6861.T","7974.T","6752.T","6954.T"]
SIM_DATA_DIR = "simulation_data"
os.makedirs(SIM_DATA_DIR, exist_ok=True)

def integrate_board_news(df):
    """板情報とニュースを統合してスコア修正"""
    for idx, row in df.iterrows():
        board_volume = fetch_board_info(row.ticker)
        news_score = fetch_latest_news(row.ticker)
        df.at[idx, "volume_change"] += board_volume/10000
        df.at[idx, "news_score"] += news_score
    return df

def pre_open_alert():
    df = build_combined_data(TICKERS)
    df = integrate_board_news(df)
    top10 = get_top_predictions(df, top_n=10)
    message = "🕗 8:40 寄り前銘柄評価\n"
    message += "\n".join([f"{r.ticker} score:{r.score}" for r in top10.itertuples()])
    send_alert(message)
    return top10

def run_simulation(top10):
    log = []
    for minute in range(0, 360, 10):  # 9:00～15:00 10分毎
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        df = build_combined_data(top10["ticker"].tolist())
        df = integrate_board_news(df)
        evaluated = evaluate_stocks(df)

        # 即時アラート判定
        for row in evaluated.itertuples():
            if row.diff_pct > 1 or row.news_score >= 2:
                send_alert(f"🚨 即時アラート: {row.ticker} | 現在株価:{row.current_price} | score:{row.score} | diff:{row.diff_pct}% | news_score:{row.news_score}")

        message = f"💬 10分毎シミュレーション ({current_time})\n"
        message += "\n".join([f"{r.ticker} action:{r.action} score:{r.score}" for r in evaluated.itertuples()])
        send_alert(message)

        log.append(evaluated)
        time.sleep(1)  # 実運用では600秒(10分)

    return log

def generate_daily_summary(log):
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    df_all = pd.concat(log)
    file_path = os.path.join(SIM_DATA_DIR, f"daily_summary_{date_str}.csv")
    df_all.to_csv(file_path, index=False)
    send_alert(f"📝 1日まとめレポート保存: {file_path}")

if __name__ == "__main__":
    top10 = pre_open_alert()
    log = run_simulation(top10)
    generate_daily_summary(log)
