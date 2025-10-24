import pandas as pd

# 例: ニューススコア + テクニカルスコアで合計scoreを計算
def evaluate_stocks(df):
    # score列がない場合は作成
    if 'score' not in df.columns:
        df['score'] = df['news_score'] + df['technical_score']

    actions = []
    for _, row in df.iterrows():
        action = "買い" if row["score"] >= 3 else ("売り" if row["score"] <= 0 else "ホールド")
        actions.append(action)
    
    df['action'] = actions
    return df
