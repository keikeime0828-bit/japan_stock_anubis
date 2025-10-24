import pandas as pd

def calculate_technical_indicators(prices):
    """簡易的なテクニカル指標算出"""
    indicators = {}
    for s, p in prices.items():
        indicators[s] = {
            'momentum': 1,   # 仮: 正なら上昇、負なら下落
            'RSI': 60,
            'MACD': 0.5,
            'bollinger': 0.2
        }
    return indicators

def select_symbols_anubis_logic():
    """①②③ロジックを統合した銘柄選定"""
    # ここでは仮の10銘柄
    return ['7203', '6758', '9984', '9433', '6971', '8035', '6752', '9432', '7267', '8306']
