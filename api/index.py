from flask import Flask, request
import json
import time
import telegram
from telegram import Bot
from telegram.ext import Updater , CommandHandler, Filters, MessageHandler, CallbackQueryHandler
import os
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, Update, InlineKeyboardMarkup

TOKEN = "5650199850:AAFACvLnysc-mwkRALoqNNTO6IW8z03XqsA"
url="https://my-beautiful-test.vercel.app/"+TOKEN
app = Flask(__name__)
app.config["SECRET_KEY"] = "mimi"
update=telegram.Update
context=telegram.ext.CallbackContext

updater = Updater(TOKEN, use_context=True)
bot=telegram.Bot(TOKEN)
bot.deleteWebhook()
time.sleep(1)
bot.setWebhook(url)


@app.route('/')
def home():
    html='''<!doctype html>
    <html>
    <head>
    </head>
    <body>
        <h2 style="color:blue">Бот простого поиска ФВ</h2>
    </body>
    </html>
    '''
    return html

@app.route('/test/'+TOKEN)
def test():
    return "ok"
    
  

@app.route("/"+TOKEN, methods=['POST'])
def hook():
   if request.method == "POST":
       #content = json.loads(request.get_data())# #WORKING
   
       chat_id=request.json["message"]["chat"]["id"]
       info=str(request.json["message"]["text"])
       greet_text="Привет. Я бот простого поиска Flowvision"
       bttons=[InlineKeyboardButton("Поиск в туториале", callback_data=3),
            InlineKeyboardButton("Поиск по статьям", callback_data=1),
            InlineKeyboardButton("Статьи по темам и отраслям", callback_data=2)
            ]
    
       keyboard=[[b] for b in bttons]
       reply_markup = InlineKeyboardMarkup(keyboard, row_width=0)
       if "start" in info:
           #bot.sendMessage(chat_id=chat_id, text=greet_text)
           bot.sendMessage(chat_id=chat_id, "Где мне поискать?", reply_markup=reply_markup)
       
       
       #chat_id="1093497662"# msg.sender_chat["username"]
       #bot.sendMessage(chat_id=chat_id, text=info)
   return "ok"
