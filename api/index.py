from flask import Flask, request
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

TOKEN = "5650199850:AAFVpNnH9pLBXQkomn-nJZlBnNucjP4s3sQ"
app = Flask(__name__)
app.config["SECRET_KEY"] = "mimi"
update=telegram.Update
context=telegram.ext.CallbackContext

updater = Updater(TOKEN, use_context=True)
bot=telegram.Bot(TOKEN)

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
       content = json.loads(request.get_data())# #WORKING
        print(content)
       
        #chat_id = request.json["message"]["chat"]["id"]
       chat_id="1093497662"# msg.sender_chat["username"]
       bot.sendMessage(chat_id=chat_id, text=str(content))
   return "ok"
    
