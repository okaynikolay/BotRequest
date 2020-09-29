import requests
import json
from datetime import datetime
import time
import telebot
import bd

CHECK_TIME = 600
BOT_TOKEN = '1203380304:AAHc29nuwOoU11mmkuMVMLvUgJryXqT8naM'

#database = адрес базы данных
#user = имя пользователя
#password = пароль
#host = хост
#port = '5432'

database = bd.TestReqBD(database, user, password, host, port)
bot = telebot.TeleBot(BOT_TOKEN)

def req(url):
    '''
    Принимает адрес сайта, возвращает статус запроса
    '''
    try:
        response = requests.get(url)
        result = response.status_code
    except Exception as ex:
        result = ex
    return result

def send_message(text, markup=None):
    admin_id = str(database.get_admin())
    bot.send_message(admin_id, text, reply_markup=markup)

def check_list(urls):
    '''
    Принимает список адресов, если у какого-либо
    адреса статус не равен 200 - отправляет
    сообщение в заданный чат тг
    '''
    for url in urls:
        status = req(url)
        if status != 200:
            ids = database.get_users()
            for id in ids:
                bot.send_message(str(id), 'Status {} for url: {}'.format(status, url))

def add_url(message):
    '''
    Принимает сообщение, добавляет адрес сайта в
    фаил с адресами,если его там нет
    '''
    url = message.text
    urls = database.get_urls()
    if url not in urls and url.split('//')[0] in ['http:', 'https:']:
        database.add_url(url)

def delete_url(message):
    url = message.text
    urls = database.get_urls()
    if url in urls:
        database.drop_url(url)

def change_target():
    try:
        target = bot.get_updates()[-1].message.chat.id
    except AttributeError:
        target = bot.get_updates()[-1].callback_query.from_user.id
    users = database.get_users()
    if int(target) not in users:
        database.add_user(int(target))
    database.change_admin(int(target))
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
                if data is not None:
                    return data
            elif atribut == 'callback':
                data = bot.get_updates()[-1].callback_query
                if data is not None:
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
        urls = database.get_urls()
        for url in urls:
            send_message(url)
    elif callback.data == 'dels':
        send_message('Введите адрес сайта, который хотите удалить:')
        mesage = status_check()
        if mesage: delete_url(mesage)

def check_id(update):
    '''
    Проверяет id пользователя в поступившем обновлении на то содержится ли он 
    в бд, если нет - добавляет его
    '''
    try:
        id = update.message.chat.id
    except AttributeError:
        id = update.callback_query.from_user.id
    users = database.get_users()
    if id not in users:
        database.add_user(int(id))

def main():
    update_time = time.time()
    check_time = time.time()
    last_update = None
    while True:
        if time.time() - check_time >= CHECK_TIME:
            urls = database.get_urls()
            check_list(urls)
            check_time = time.time()
            

        if time.time() - update_time >= 5:
            try:
                update = bot.get_updates()[-1]
            except:
                update = False
            if update:
                check_id(update)
                keyboard = telebot.types.InlineKeyboardMarkup()
                new_data = telebot.types.InlineKeyboardButton(text='Добавить новый сайт', callback_data='new')
                keyboard.add(new_data)
                all_data = telebot.types.InlineKeyboardButton(text='Показать все сайты', callback_data='alls')
                keyboard.add(all_data)
                dal_data = telebot.types.InlineKeyboardButton(text='Удалить сайт', callback_data='dels')
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
