learning_db = {}

def update_learning(ticker, data):
    if ticker not in learning_db:
        learning_db[ticker] = []
    learning_db[ticker].append(data)

def get_top_predictions(df, top_n=10):
    """diff_pct, volume_change, news_score, 急騰アラートを統合して精密スコア計算"""
    df["score"] = df["diff_pct"] + df["volume_change"]/10 + df["news_score"]*1.5
    df.loc[df["alerts"]=="株価急騰","score"] += 2
    top_df = df.sort_values("score", ascending=False).head(top_n)
    return top_df

def evaluate_stocks(df):
    """買い/売り/ホールド判定"""
    evaluations = []
    for idx, row in df.iterrows():
        score = row["score"]
        action = "買い" if score >= 3 else ("売り" if score <= 0 else "ホールド")
        evaluations.append({"ticker": row["ticker"], "score": score, "action": action})
    return pd.DataFrame(evaluations).merge(df, on="ticker")
