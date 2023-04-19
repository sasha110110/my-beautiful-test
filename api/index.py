from flask import Flask, request
import json
import telegram
from telegram import Bot
from telegram.ext import Updater , CommandHandler, Filters, MessageHandler, CallbackQueryHandler
import os
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, Update, InlineKeyboardMarkup

TOKEN = "5650199850:AAFVpNnH9pLBXQkomn-nJZlBnNucjP4s3sQ"
app = Flask(__name__)
app.config["SECRET_KEY"] = "mimi"
update=telegram.Update
context=telegram.ext.CallbackContext

updater = Updater(TOKEN, use_context=True)
bot=telegram.Bot(TOKEN)
dp = updater.dispatcher

CHAT_TO = ""


@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/test')
def test():
    
    bttons=[InlineKeyboardButton("Поиск в туториале", callback_data=3),
            InlineKeyboardButton("Поиск по статьям", callback_data=1),
            InlineKeyboardButton("Статьи по темам и отраслям", callback_data=2)
            ]
    
    keyboard=[[b] for b in bttons]
    reply_markup = InlineKeyboardMarkup(keyboard, row_width=0)
    update.message.reply_text("Где мне поискать?", reply_markup=reply_markup)
    chat_id="1093497662"# msg.sender_chat["username"]
    bot.sendMessage(chat_id=chat_id, text="test")
    
  

@app.route("/"+TOKEN, methods=['POST'])
def hook():
   if request.method == "POST":
       
       content = json.loads(request.get_data())# #WORKING
       print(content)
       
        ##chat_id = request.json["message"]["chat"]["id"]
       chat_id="1093497662"# msg.sender_chat["username"]
       bot.sendMessage(chat_id=chat_id, text=str(content))
   return "ok"
    
