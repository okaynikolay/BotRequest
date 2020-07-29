import requests
import json
from telebot import types
from datetime import datetime
import time
import telebot

BOT_TOKEN = "1324460923:AAHfXx4AW1pCmxa9figy5EKgkCbnS7xzo74"

try:
    with open('chat_id.txt') as f:
        CHAT_ID = f.readline().strip()
except FileNotFoundError:
    CHAT_ID = '483882071' # чат для обратной связи

bot = telebot.TeleBot(BOT_TOKEN)

def req(url):
    '''
    Принимает адрес сайта, возвращает статус запроса
    '''
    response = requests.get(url)
    return response.status_code

def send_message(text, markup=None):
    try:
        with open('chat_id.txt') as f:
            chat_id = f.readline().strip()
    except FileNotFoundError:
        chat_id = change_target()
    bot.send_message(chat_id, text, reply_markup=markup)

def check_list(urls):
    '''
    Принимает список адресов, если у какого-либо
    адреса статус не равен 200 - отправляет
    сообщение в заданный чат тг
    '''
    for url in urls:
        status = req(url)
        if status != 200:
            send_message('Status {} for url: {}'.format(status, url))

def add_url(message):
    '''
    Принимает сообщение, добавляет адрес сайта в
    фаил с адресами,если его там нет
    '''
    with open('urls.json') as f:
        js = json.load(f)
    if message.text not in js:
        with open('urls.json', 'w') as f:
            js[message.text] = len(js.values())
            json.dump(js, f)

def delete_url(message):
    url = message.text
    with open('urls.json') as f:
        js = json.load(f)
        if url in js:
            js.pop(url)
    with open('urls.json', 'w') as f:
        json.dump(js, f)

def change_target():
    try:
        target = bot.get_updates()[-1].message.chat.id
    except AttributeError:
        target = bot.get_updates()[-1].callback_query.from_user.id
    with open('chat_id.txt', 'w') as f:
        f.write(str(target))
    return str(target)
    

def status_check(atribut = 'message'):
    '''
    На вход подается атрибут, который может принимать значения message, 
    callback и date. проводит проверку раз в 5 секунд в течении 30 секунд
    на наличие в updates объекта, соответствующего атрибуту. В случае 
    появления объекта - возвращает его, если не обнаружит - вернет False
    '''
    now = time.time()
    while time.time() - now < 30:
        time.sleep(2)
        try:
            if atribut == 'message':
                data = bot.get_updates()[-1].message
                return data
            elif atribut == 'callback':
                data = bot.get_updates()[-1].callback_query
                return data
        except AttributeError:
            pass
    return False   

def callback_check():
    '''
    Обработчик кнопок
    '''
    callback = status_check('callback')
    if not callback:
        return
    if callback.data == 'new':
        send_message('Введите адрес сайта')
        message = status_check()
        if message: add_url(message) 
                 
    elif callback.data == 'alls':
        with open('urls.json') as f:
            js = json.load(f)
        for i in js.keys():
            send_message(i)
    elif callback.data == 'dels':
        send_message('Введите адрес сайта, который хотите удалить:')
        mesage = status_check()
        if mesage: delete_url(mesage)

def main():
    update_time = time.time()
    check_time = time.time()
    last_update = None
    while True:
        if time.time() - check_time >= 3600:
            with open('urls.json') as f:
                urls = json.load(f)
            check_list(urls)
            check_time = time.time()

        if time.time() - update_time >= 5:
            try:
                update = bot.get_updates()[-1]
            except:
                update = False
            if update:
                keyboard = types.InlineKeyboardMarkup()
                new_data = types.InlineKeyboardButton(text='Добавить новый сайт', callback_data='new')
                keyboard.add(new_data)
                all_data = types.InlineKeyboardButton(text='Показать все сайты', callback_data='alls')
                keyboard.add(all_data)
                dal_data = types.InlineKeyboardButton(text='Удалить сайт', callback_data='dels')
                keyboard.add(dal_data)
                if update.message is not None:
                    if update.message.text == '/target':
                        change_target()
                    send_message('Здравствуйте.', markup=keyboard)
                time.sleep(2)
                callback_check()
            
            
                last_update = bot.get_updates()[-1].update_id
                bot.get_updates(offset=last_update+1)
            update_time = time.time()
        

if __name__ == '__main__':
    main()
