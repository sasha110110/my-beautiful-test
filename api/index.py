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

CHAT_TO = ""


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

@app.route('/test')
def test():
    chat_id="1093497662"# msg.sender_chat["username"]
    bot.sendMessage(chat_id=chat_id, text="test")
    
   
  

@app.route("/"+TOKEN, methods=['POST'])
def hook():
    global bot
    if request.method == "POST":
        content = json.loads(request.get_data())# #WORKING
        print(content)
       
        #chat_id = request.json["message"]["chat"]["id"]
        chat_id="1093497662"# msg.sender_chat["username"]
        bot.sendMessage(chat_id=chat_id, text=str(content))
   return "ok"
    
