import requests
import telebot
from telebot.types import *
import json

bot = telebot.TeleBot('5915797891:AAHiXjpHS8AVpWJ04bSy0DOznAnmq4qJMrE')

PRODUCT_STRING = 'Id: %id% Name: %name% Price: %price%\nPhoto: %photo%'


@bot.message_handler(commands=['products'])
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

@bot.message_handler(commands=['register'])
def products_command_handler(message: Message):
    res = requests.get('https://functions.yandexcloud.net/d4e07kfsoq37d9l5ikdk?id='+str(message.chat.id))
    if res.text == 'True':
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы')
        return
    args = message.text.split()
    if len(args) > 2:
        name = args[1]
        email = args[2]
        res = requests.get('https://functions.yandexcloud.net/d4ec8ap2db8738u55tri?id='+str(message.chat.id)+'&email='+email+'&name='+name)
        if res.text != 'ok':
            bot.send_message(message.chat.id, 'Ипользуйте: /register name email')
            return
        bot.send_message(message.chat.id, 'Вы успешно зарегистрированы')
    else:
        bot.send_message(message.chat.id, 'Ипользуйте: /register name email')

@bot.message_handler(commands=['dregister'])
def products_command_handler(message: Message):
    res = requests.get('https://functions.yandexcloud.net/d4e0rlplqnl2t0p3cqh5?id='+str(message.chat.id))
    if res.text == 'True':
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы')
        return
    args = message.text.split()
    if len(args) > 2 and args[1].isdigit() and args[2].isdigit():
        x = args[1]
        y = args[2]
        res = requests.get('https://functions.yandexcloud.net/d4ef9kk5km8fde01gnjp?id='+str(message.chat.id)+'&location={"x":'+x+',"y":'+y+'}')
        if res.text != 'ok':
            bot.send_message(message.chat.id, 'Ипользуйте: /dregister x y')
            return
        bot.send_message(message.chat.id, 'Вы успешно зарегистрированы')
    else:
        bot.send_message(message.chat.id, 'Ипользуйте: /dregister x y')


@bot.message_handler(commands=['mydelivery'])
def products_command_handler(message: Message):
    res = requests.get('https://functions.yandexcloud.net/d4e61jpj3sfgqpo0qirj?id=' + str(message.chat.id))
    if res.text == 'False':
        bot.send_message(message.chat.id, 'Вы не доставщик')
        return
    res = requests.get('https://functions.yandexcloud.net/d4e61jpj3sfgqpo0qirj?id=' + str(message.chat.id))
    print(res.text)
    json_object = json.loads(str(res.text.replace("': b'", "': '").replace('"','#').replace("'", '"').replace('#',"'")))
    if len(json_object) <= 0:
        bot.send_message(message.chat.id, 'У вас нет доставок')
        return

    for i in json_object:
        bot.send_message(message.chat.id,
                         '#ЗАКАЗ\nproduct:' + str(i['product_id']) + ' stock_id:' + str(i['stock_id']) + '\nprice:' +
                         str(i['price']) + '\ncoordinate: ' + i['coordinate'])


@bot.message_handler(commands=['order'])
def products_command_handler(message: Message):
    res = requests.get('https://functions.yandexcloud.net/d4e07kfsoq37d9l5ikdk?id='+str(message.chat.id))
    json_object = json.loads(str(res.text.replace("': b'", "': '").replace("'", '"')))
    args = message.text.split()
    if len(json_object) > 0:
        productId = args[1]
        x = args[2]
        y = args[3]
        res = requests.get('https://functions.yandexcloud.net/d4et80slfr0rsp5h7gq7?product_id='+str(productId)+'&count=1')
        json_object_stock = json.loads(str(res.text.replace("': b'", "': '").replace("'", '"')))
        if len(json_object_stock) == 0:
            bot.send_message(message.chat.id, 'Данного товара нет ни на одном складе')
            return

        res = requests.get('https://functions.yandexcloud.net/d4ebuth672ccf2f4i5fp?id='+str(message.chat.id))
        json_object = json.loads(str(res.text.replace("': b'", "': '").replace("'", '"')))
        email = json_object[0]['email']
        res = requests.get('https://functions.yandexcloud.net/d4e5gmpvpe3mmvdjplvr?productId='+str(productId)+'&stockId='+str(json_object_stock[0]['stock_id'])+'&userId='+str(message.chat.id)+'&coordinate={"x":'+x+',"y":'+y+'}')
        if res.status_code != 200:
            bot.send_message(message.chat.id, 'Ипользуйте: /order productId x y')
            return
        bot.send_message(int(res.text), 'У вас новая доставка:\nx:'+x+' y:'+y+'\nemail: '+email+'\nproductId: '+productId)
        res = requests.get('https://functions.yandexcloud.net/d4ebuth672ccf2f4i5fp?id='+str(res.text))
        json_object = json.loads(str(res.text.replace("': b'", "': '").replace("'", '"')))
        bot.send_message(message.chat.id, 'Заказ создан. Вам его доставит '+json_object[0]['name']+' ('+json_object[0]['email']+')')
    else:
        bot.send_message(message.chat.id, 'У вас нет доставок')


bot.infinity_polling()
