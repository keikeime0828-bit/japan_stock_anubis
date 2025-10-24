import os
import pandas as pd
import datetime
from fetch_data import get_realtime_prices, get_board_info, get_news_materials
from utils import select_symbols_anubis_logic, calculate_technical_indicators

# -----------------------------
# 設定
# -----------------------------
DATA_DIR = 'data'
LOG_DIR = 'logs'
LEARNING_FILE = os.path.join(DATA_DIR, 'learning_record.csv')
SELECTED_SYMBOLS = []  # ①②③で選定された銘柄

# ディレクトリ作成
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ログファイル
log_file = os.path.join(LOG_DIR, f'daily_{datetime.date.today().strftime("%Y%m%d")}.log')

def log(msg):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {msg}")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

# -----------------------------
# 学習記録の読み込み（空ファイル対策）
# -----------------------------
if os.path.exists(LEARNING_FILE):
    try:
        learning_df = pd.read_csv(LEARNING_FILE)
        if learning_df.empty:
            learning_df = pd.DataFrame(columns=['date','symbol','sim_price','real_price','discrepancy'])
    except pd.errors.EmptyDataError:
        learning_df = pd.DataFrame(columns=['date','symbol','sim_price','real_price','discrepancy'])
else:
    learning_df = pd.DataFrame(columns=['date','symbol','sim_price','real_price','discrepancy'])

# -----------------------------
# 1日分シミュレーション
# -----------------------------
def simulate_day():
    global SELECTED_SYMBOLS
    selected_symbols = select_symbols_anubis_logic()
    SELECTED_SYMBOLS = selected_symbols[:10]  # 厳選10銘柄
    log(f"Selected Symbols: {SELECTED_SYMBOLS}")

    # 仮想ポジション初期化
    vt_positions = {s: 0 for s in SELECTED_SYMBOLS}

    # シミュレーションタイムフロー（8:40～15:00まで10分毎）
    sim_times = pd.date_range("08:40", "15:00", freq="10min").time

    for t in sim_times:
        prices = get_realtime_prices(SELECTED_SYMBOLS)
        board = get_board_info(SELECTED_SYMBOLS)
        news = get_news_materials(SELECTED_SYMBOLS)

        indicators = calculate_technical_indicators(prices)

        for s in SELECTED_SYMBOLS:
            # 買い/売り/ホールド判定（例）
            if indicators[s]['momentum'] > 0 and board[s]['buy_pressure'] > 0.6:
                vt_positions[s] += 100
            elif indicators[s]['momentum'] < 0 and vt_positions[s] > 0:
                vt_positions[s] -= 100

        # 乖離計算と学習記録更新
        for s in SELECTED_SYMBOLS:
            sim = vt_positions[s] * prices[s]
            real = prices[s]
            discrepancy = (sim - real) / real

            # 無限大や過大数値防止
            if abs(discrepancy) > 1:
                discrepancy = 0.0

            vt_positions[s] = int(vt_positions[s] * (1 - discrepancy))

            learning_df.loc[len(learning_df)] = {
                'date': datetime.date.today(),
                'symbol': s,
                'sim_price': sim,
                'real_price': real,
                'discrepancy': discrepancy
            }

        log(f"Time {t} | Positions: {vt_positions} | Prices: {prices}")

    learning_df.to_csv(LEARNING_FILE, index=False)
    log("Day simulation complete and learning record updated.")

if __name__ == "__main__":
    simulate_day()
