import requests
from bs4 import BeautifulSoup

def fetch_stock_price(symbol):
    url = f"https://www.google.com/finance/quote/{symbol}:TYO"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        price_tag = soup.select_one('div.YMlKec.fxKbKc')
        price = float(price_tag.text.replace(',', ''))
    except:
        price = None
    return price

def fetch_news(symbol, max_items=5):
    url = f"https://www.google.com/finance/quote/{symbol}:TYO"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    news_items = []
    for item in soup.select('div.CCw2Fe')[:max_items]:
        title = item.get_text(strip=True)
        news_items.append(title)
    return news_items
