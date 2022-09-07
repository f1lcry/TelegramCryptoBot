import json
import requests
from googletrans import Translator
from coinmarketcapapi import CoinMarketCapAPI
from bs4 import BeautifulSoup
from random import choice

"""CLASS Article grabber"""


class GrabberArticle:
    url = ""
    filename = ""
    path = ""
    content_tags = ['a']
    wrap = 80
    url_key = ""

    def __init__(self, article_url, url_key):
        self.url = article_url
        self.url_key = url_key

    """FUNCTION Get 3 recent top news from website"""

    def get_text(self):
        r = requests.get(self.url).text
        soup = BeautifulSoup(r, features="html.parser")
        content = soup.find_all(self.content_tags)
        articles = []
        for a in content:
            if 'class' in a.attrs:
                if 'title' in a['class']:
                    articles.append(str("<a href='" + self.url_key + a['href'] + "'>") + a.text + "</a>")
        articles = articles[:3]
        result = f"⚡️ {articles[0]} \n\n🤓 {articles[1]} \n\n🔥 {articles[2]}"

        print("Creating a message... Progress: 100%")

        return result


"""FUNCTION Get fear and greed index"""


def get_fng_index():
    url = "https://api.alternative.me/fng/?limit=0"
    translator = Translator()

    data = requests.get(url)
    data = data.json()
    fng_index = data['data'][0]['value']
    fng_index_classification = translator.translate(str(data['data'][0]['value_classification']), src="en",
                                                    dest="ru").text

    print("Creating a message... Progress: 60%")

    return f"Индекс страха и жадности: {fng_index} - {fng_index_classification}"


"""FUNCTION Round price with 3 first numbers aren't rounded"""


def round_price(price):
    price = int(price)
    digits = len(str(price)) - 3

    return int(round(price, -digits))


"""FUNCTION Short price with word definition of number's digits"""


def short_price(rounded_price):
    result = str(rounded_price)
    number_classification = ""

    if rounded_price > 999:
        nulls = 0
        str_price = str(int(rounded_price))
        digits = len(str_price) // 3
        if len(str_price) % 3 == 0:
            digits -= 1
            cut_number = int(int(str_price) / 1000 ** digits)
        else:
            nulls = digits * 3
            digit_numbers_count = len(str_price) - nulls
            cut_number = round(int(str_price) / 1000 ** digits, 3 - digit_numbers_count)

        if digits == 1:
            number_classification = "тыс."
        elif digits == 2:
            number_classification = "мил."
        elif digits == 3:
            number_classification = "млрд."
        elif digits == 4:
            number_classification = "трлн."
        result = str(cut_number) + " " + number_classification

    return result


"""FUNCTION Get average prices of lead coins"""


def get_prices():
    result = ""
    key = "https://api.binance.com/api/v3/ticker/price?symbol="
    currencies = {"BTCUSDT": "Биткоин", "ETHUSDT": "Эфир", "SOLUSDT": "Солана"}

    for i in currencies:
        url = key + i
        data = requests.get(url)
        data = data.json()
        price = float(data["price"])
        result += currencies[i] + " ~$" + short_price(round_price(price)) + "\n"

    print("Creating a message... Progress: 45%")

    return result


"""FUNCTION Get 24h vol and Dominance"""


def get_global_market_info():
    cmc = CoinMarketCapAPI('b44c1fd8-1c05-45b9-8df7-380a409f9b69')
    global_quote = cmc.globalmetrics_quotes_latest()
    global_quote = global_quote.data
    vol = short_price(round_price(global_quote['quote']['USD']['total_volume_24h']))
    market_cap = short_price(round_price(global_quote['quote']['USD']['total_market_cap']))
    btc_dominance = round(global_quote['btc_dominance'], 1)
    eth_dominance = round(global_quote['eth_dominance'], 1)

    print("Creating a message... Progress: 81%")

    return f'Капитализация рынка: ~${market_cap}' + f'\n24ч Объём: ~${vol}' + f"\nДоминация:\n- Биткоин: {btc_dominance}%\n- Эфир: {eth_dominance}%"


"""FUNCTION Recognize the market's trend"""


def recognize_trend():
    price_changes = []
    result = ""
    key = "https://api.binance.com/api/v3/ticker/24hr?symbol="
    currencies = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT",
                  "SOLUSDT", "DOGEUSDT", "DOTUSDT", "MATICUSDT", "AVAXUSDT"]
    for i in currencies:
        url = key + i
        data = requests.get(url)
        data = data.json()
        change_percent = float(data["priceChangePercent"])
        if change_percent < -0.5:
            price_changes.append("-")
        elif -0.5 <= change_percent <= 0.5:
            price_changes.append("=")
        else:
            price_changes.append("+")

    if price_changes.count("=") >= 5 or abs(price_changes.count("+") - price_changes.count("-")) <= 2:
        result = choice(["Рынок в боковике. Часть альтов зелёные, часть красные.🟥🟩",
                         "Рынок во флэте. Половина аьлтов в плюсе, половина в минусе.🟥🟩",
                         "Рынок остался прежним. Какие-то альты подросли, какие-то снизились.🟥🟩"])
    elif price_changes.count("-") - price_changes.count("+") > 1:
        result = choice(["Рынок в минусе. Большая часть альтов красные.🟥",
                         "Рынок снизился. Большая часть аьлтов в минусе.🟥",
                         "Рынок сегодня в минусе. Большинство альтов снизились.🟥"])
    else:
        result = choice(["Рынок в плюсе. Большая часть альтов выросли.🟩",
                         "Рынок подрос. Большинство алтов в плюсе.🟩",
                         "Рынок сегодня в плюсе. Большая часть альтов зелёные.🟩"])

    print("Creating a message... Progress: 30%")

    return result


# print(get_prices())

# print(get_fng_index())

# print(get_global_market_info())

# news_url = 'https://cryptonews.net/news/top/'
# news_url_key = 'http://www.cryptonews.net'
# grabber = GrabberArticle(news_url, news_url_key)
# print(grabber.get_text())

# print(recognize_trend())
