import requests
import telebot
from telebot.types import *
import json

bot = telebot.TeleBot('5915797891:AAHiXjpHS8AVpWJ04bSy0DOznAnmq4qJMrE')

PRODUCT_STRING = 'Id: %id% Name: %name% Price: %price%\nPhoto: %photo%'


@bot.message_handler(commands=['start'])
def products_command_handler(message: Message):
    res = requests.get('https://functions.yandexcloud.net/d4ecm6a80hvt9rrs7mmk')
    json_object = json.loads(str(res.text.replace("': b'", "': '").replace("'", '"')))
    for i in json_object:
        print(i)
        bot.send_message(message.chat.id, PRODUCT_STRING
                         .replace('%id%', str(i['id']))
                         .replace('%name%', str(i['name']))
                         .replace('%price%', str(i['price']))
                         .replace('%photo%', str(i['photoUrl']))
                         )


bot.infinity_polling()
