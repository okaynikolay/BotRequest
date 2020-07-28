import requests
import json
from telebot import types
from datetime import datetime
import time
import telebot

BOT_TOKEN = "1324460923:AAHfXx4AW1pCmxa9figy5EKgkCbnS7xzo74"

CHAT_ID = '483882071' # чат для обратной связи

bot = telebot.TeleBot(BOT_TOKEN)

def req(url):
    '''
    Принимает адрес сайта, возвращает статус запроса
    '''
    response = requests.get(url)
    return response.status_code

def check_list(urls):
    '''
    Принимает список адресов, если у какого-либо
    адреса статус не равен 200 - отправляет
    сообщение в заданный чат тг
    '''
    for url in urls.values():
        status = req(url)
        if status != 200:
            bot.send_message(CHAT_ID, 'Status {} for url: {}'.format(status, url))

def add_url(message):
    '''
    Принимает сообщение, добавляет адрес сайта в
    фаил с адресами,если его там нет
    '''
    with open('urls.json') as f:
        js = json.load(f)
    if message.text not in js.values():
        with open('urls.json', 'w') as f:
            js[len(js)] = message.text
            json.dump(js, f)

def send_message(chat_id=CHAT_ID, text):
    bot.send_message(chat_id, text)

def callback_check():
    callback = bot.get_updates[-1].callback_query
    if callback.data == 'new':
        send_message(

def main():
    update_time = time.time()
    check_time = time.time()
    while True:
        if time.time() - check_time >= 30:
            with open('urls.json') as f:
                urls = json.load(f)
            check_list(urls)
            check_time = time.time()

        if time.time() - update_time >= 20: 
            message = bot.get_updates()[-1].message
            if time.time() - message.date < 30:
                keyboard = types.InlineKeyboardMarkup()
                new_data = types.InlineKeyboardButton(text='Добавить новый сайт', callback_data='new')
                keyboard.add(new_data)
                all_data = types.InlineKeyboardButton(text='Показать все сайты', callback_data='alls')
                keyboard.add(all_data)
                dal_data = types.InlineKeyboardButton(text='Удалить сайт', callback_data='dels')
                keyboard.add(dal_data)
                bot.send_message(CHAT_ID, 'Здравствуйте.', reply_markup=keyboard)

            if message.text.split('//')[0] in ['http:','https:']: 
                add_url(message)
            update_time = time.time()
        

if __name__ == '__main__':
    main()
