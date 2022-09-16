import time

from bot_functions import get_fng_index, get_prices, get_global_market_info, recognize_trend
from bot_functions import GrabberArticle

import telebot
import json
import requests

from time import sleep
from datetime import datetime
from threading import Thread


BOT_TOKEN = ""
CHANNEL_NAME = "@testinfochannelpci"
news_url = 'https://cryptonews.net/news/top/'
news_url_key = 'http://www.cryptonews.net'
market_image = "https://ibb.co/1sJ8m5B"
bot = telebot.TeleBot(BOT_TOKEN)
grabber = GrabberArticle(news_url, news_url_key)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "You can get the global market info by clicking a button /getmarketinfo and ask me about coins rates "
                 "by sending the coin's symbol. Example: 'BTC'")


@bot.message_handler(commands=['getmarketinfo'])
def get_market_info(message):
    info = "Привет! \U0001F31E Ежедневный обзор рынка: \n\n" + recognize_trend() + "\n\n" + get_prices() + "\n" + get_fng_index() + "\n\n" + get_global_market_info() + "\n\n" + grabber.get_text()
    # bot.send_photo(message.from_user.id, fng_image, caption=info, parse_mode="HTML")
    bot.send_photo(CHANNEL_NAME, market_image, caption=info, parse_mode="HTML")


@bot.message_handler(func=lambda m: True)
def say_price(message):
    # print(message.text.split())
    key = "https://api.binance.com/api/v3/ticker/price?symbol="
    coin_pair = message.text + "USDT"
    url = key + coin_pair
    data = requests.get(url)
    data = data.json()
    price = round(float(data['price']), 4) if float(data['price']) > 100 else float(data['price'])
    bot.reply_to(message, "{0} price is ${1:,}".format(data['symbol'], price).replace(',', ' '))
    bot.send_message(CHANNEL_NAME, "Price is asked")


def sleep_poster():
    while True:
        sleep(30)
        now = time.localtime()
        if now.tm_hour == 5 and now.tm_min == 0:
            print("Creating a message... Progress: 5%")
            info = "Доброе утро! \U0001F31E Ежедневный обзор рынка: \n\n" + recognize_trend() + "\n\n" + get_prices() + "\n" + get_fng_index() + "\n\n" + get_global_market_info() + "\n\n" + grabber.get_text()
            bot.send_photo(CHANNEL_NAME, market_image, caption=info, parse_mode="HTML")
            print('Отправили сообщение!')


print("Bot started")

thr = Thread(target=sleep_poster)
thr.run()

bot.polling(none_stop=True)
