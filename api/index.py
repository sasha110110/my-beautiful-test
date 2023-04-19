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

def help(update, context):
    global CHAT_TO
    CHAT_TO=update.message.chat_id
    text="Я бот простого поиска. Ищу по ключевым словам и темам на сайте и в туториале. Просто напиши что искать"
    context.bot.sendMessage(text=text, chat_id=CHAT_TO)
def greet(update, context):
    global CHAT_TO
    CHAT_TO=update.message.chat_id
    text="Hiiiii"
    context.bot.sendMessage(text=text, chat_id=CHAT_TO)
    
proc_handler= MessageHandler(Filters.text & (~Filters.command) , process_msg)
greet_handler=CommandHandler("start", greet)
#query_handler=CallbackQueryHandler(first_choice)

   
dp.add_handler(proc_handler)
dp.add_handler(greet_handler)
#dp.add_handler(query_handler, group=1)
    

    

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/test')
def test():
    chat_id="1093497662"# msg.sender_chat["username"]
    bot.sendMessage(chat_id=chat_id, text="test")
    
  

@app.route("/"+TOKEN, methods=['POST'])
def hook():
   if request.method == "POST":
       dp.processUpdate(json.loads(request.get_data()))
       #content = json.loads(request.get_data())# #WORKING
       #print(content)
       
        ##chat_id = request.json["message"]["chat"]["id"]
       #chat_id="1093497662"# msg.sender_chat["username"]
       #bot.sendMessage(chat_id=chat_id, text=str(content))
   return "ok"
    
