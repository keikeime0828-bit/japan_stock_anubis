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
# 学習記録の読み込み
# -----------------------------
if os.path.exists(LEARNING_FILE):
    learning_df = pd.read_csv(LEARNING_FILE)
else:
    learning_df = pd.DataFrame(columns=['date','symbol','sim_price','real_price','discrepancy'])

# -----------------------------
# 1日分シミュレーション
# -----------------------------
def simulate_day():
    # ①②③ロジックで銘柄選定
    global SELECTED_SYMBOLS
    selected_symbols = select_symbols_anubis_logic()
    SELECTED_SYMBOLS = selected_symbols[:10]  # 厳選10銘柄
    log(f"Selected Symbols: {SELECTED_SYMBOLS}")

    # 仮想ポジション初期化
    vt_positions = {s: 0 for s in SELECTED_SYMBOLS}

    # シミュレーションタイムフロー（8:40～15:00まで10分毎）
    sim_times = pd.date_range("08:40", "15:00", freq="10min").time

    for t in sim_times:
        # リアル株価・板情報・材料取得
        prices = get_realtime_prices(SELECTED_SYMBOLS)
        board = get_board_info(SELECTED_SYMBOLS)
        news = get_news_materials(SELECTED_SYMBOLS)

        # テクニカル計算
        indicators = calculate_technical_indicators(prices)

        # 仮想取引（単純例：板・材料・指標で売買判定）
        for s in SELECTED_SYMBOLS:
            # ここで買い/売り/ホールド判定を実施
            # 実装例: 上昇モメンタム & 板買い優勢なら買い
            if indicators[s]['momentum'] > 0 and board[s]['buy_pressure'] > 0.6:
                vt_positions[s] += 100  # 100株買い
            elif indicators[s]['momentum'] < 0 and vt_positions[s] > 0:
                vt_positions[s] -= 100  # 100株売り

        # 乖離計算と学習記録更新
        for s in SELECTED_SYMBOLS:
            sim = vt_positions[s] * prices[s]
            real = prices[s]
            discrepancy = (sim - real) / real
            if abs(discrepancy) > 0.01:
                vt_positions[s] = int(vt_positions[s] * (1 - discrepancy))  # 調整
            # 学習データ追加
            learning_df.loc[len(learning_df)] = {
                'date': datetime.date.today(),
                'symbol': s,
                'sim_price': sim,
                'real_price': real,
                'discrepancy': discrepancy
            }

        log(f"Time {t} | Positions: {vt_positions} | Prices: {prices}")

    # 学習結果保存
    learning_df.to_csv(LEARNING_FILE, index=False)
    log("Day simulation complete and learning record updated.")

if __name__ == "__main__":
    simulate_day()
