learning_db = {}

def update_learning(ticker, data):
    if ticker not in learning_db:
        learning_db[ticker] = []
    learning_db[ticker].append(data)

def get_top_predictions(df, top_n=10):
    df["score"] = df["diff_pct"] + df["volume_change"]/10 + df["news_score"]*1.5
    df.loc[df["alerts"]=="株価急騰","score"] += 2
    top_df = df.sort_values("score", ascending=False).head(top_n)
    return top_df

def evaluate_stocks(df):
    evaluations = []
    for idx, row in df.iterrows():
        action = "買い" if row["score"] >= 3 else ("売り" if row["score"] <= 0 else "ホールド")
        evaluations.append({"ticker": row["ticker"], "score": row["score"], "action": action})
    return pd.DataFrame(evaluations).merge(df, on="ticker")
