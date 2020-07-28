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
print(bot.get_updates()[-1].message.text)
'''
url ='http://www.example.org/index.asp'
#print(code(url))
def timer(start):
    while


@bot.message_handler()
def txt(message):
    print(message.text)
    timer(message.date)
bot.polling()
