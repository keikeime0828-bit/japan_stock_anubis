import requests
from bs4 import BeautifulSoup

def fetch_board_info(ticker):
    """株板情報・出来高急騰判定"""
    url = f"https://finance.yahoo.co.jp/quote/{ticker}"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    # 簡易例: 出来高取得
    volume_tag = soup.find("th", text="出来高")
    if volume_tag:
        volume = volume_tag.find_next_sibling("td").text
        return int(volume.replace(",", ""))
    return 0

def fetch_latest_news(ticker):
    """ニュース・好材料判定"""
    url = f"https://finance.yahoo.co.jp/quote/{ticker}/news"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    news_items = soup.select("li > a")
    news_score = 0
    for item in news_items[:5]:  # 最新5件評価
        text = item.get_text()
        if any(k in text for k in ["増益", "受注", "好材料", "上方修正"]):
            news_score += 1
    return news_score
