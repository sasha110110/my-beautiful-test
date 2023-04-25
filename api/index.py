from flask import Flask, request
import json
import time
import telegram
from telegram import Bot
from telegram.ext import Updater , CommandHandler, Filters, MessageHandler, CallbackQueryHandler
import os
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, Update, InlineKeyboardMarkup
import pandas as pd
from api.df_all_articles import df_list

#base_dir = os.path.dirname(os.path.abspath(__file__))
df_articles = pd.read_csv('/data/df_all_articles.csv')
#with open(os.path.join("data", "df_all_articles.json", 'r')) as f:
    #df_all_a_list = json.load(f)
#df_tutorial = pd.read_csv("/data/FV_tutorial.csv")
df_articles = pd.DataFrame(df_list, columns=["Q", "link", "category"])

GLOBAL_SEARCH=""


def is_similar(query, string):
    list_of_words=query.split()
    new_list=[word[:-2] for word in list_of_words if len(word)>=5]
    num_of_contained_words_list=[]
    num_of_contained_words=0
    for word in new_list:
        if (isinstance(string, str)):
              if word in string:
                  num_of_contained_words+=1
        else:
          pass
    return num_of_contained_words

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
    msg_counter=0
   
    if request.method == "POST":
        
       #content = json.loads(request.get_data())# #WORKING
   
       chat_id=request.json["message"]["chat"]["id"]
       info=str(request.json["message"]["text"])
       greet_text="Привет. Я бот простого поиска Flowvision"
       # keyboard=[["Поиск в туториале", 
                 # "Поиск по статьям", 
              #  "Статьи по темам"]]
    
       #keyboard=[[b] for b in bttons]
       #reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
       bttons=[InlineKeyboardButton("Поиск в туториале", callback_data=3),
            InlineKeyboardButton("Поиск по статьям", callback_data=1),
            InlineKeyboardButton("Статьи по темам и отраслям", callback_data=2)
            ]
    
       keyboard=[[b] for b in bttons]
       reply_markup = InlineKeyboardMarkup(keyboard, row_width=0)
       
       if "start" in info:
           #bot.sendMessage(chat_id=chat_id, text=greet_text)
           bot.sendMessage(chat_id, "Где мне поискать?", reply_markup=reply_markup)
           msg_counter+=1
       if "callback_query" in request.json:
           bot.sendMessage(chat_id, text=str(request.json))
            
        
       if "Поиск в туториале" in info:
           pass
       
       if "Поиск по статьям" in info:
          pass
    
       if "Статьи по темам" in info:
          pass
       
       
       #chat_id="1093497662"# msg.sender_chat["username"]
       #bot.sendMessage(chat_id=chat_id, text=info)
    return "ok"
