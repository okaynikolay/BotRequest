import time
import telebot
import requests
import json

BOT_TOKEN = "1324460923:AAHfXx4AW1pCmxa9figy5EKgkCbnS7xzo74"
bot = telebot.TeleBot(BOT_TOKEN)
def code(url):
    return requests.get(url).status_code
'''
with open('urls.json') as f:
    urls = json.load(f)
for url in urls.values():
    print(url)
    print(requests.get(url).status_code)


print(bot.get_updates()[-1].message.chat.id)
'''
print(bot.get_updates(limit=1)[0].message.date)
