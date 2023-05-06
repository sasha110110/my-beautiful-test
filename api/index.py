from flask import Flask, request, session
import json
import time
import telegram
from telegram import Bot
from telegram.ext import Updater , CommandHandler, Filters, MessageHandler, CallbackQueryHandler
import os
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, Update, InlineKeyboardMarkup
import pandas as pd
from io import StringIO
from api.df_all_articles import df_list


#base_dir = os.path.dirname(os.path.abspath(__file__))
global df_articles
global df_tutorial
global GLOBAL_SEARCH
df_articles=pd.read_csv(os.path.join("data", "df_all_articles.csv"))
df_tutorial=pd.read_csv(os.path.join("data", "fv_tutorial.csv"))
df_articles.apply(lambda x: x.astype(str).str.lower())
df_tutorial.apply(lambda x: x.astype(str).str.lower())

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
    
@app.route('/check')
def check():
    global df_articles
    bot.sendMessage(chat_id="1093497662", text=str(df_articles.head(2).values))
    
    
  

@app.route("/"+TOKEN, methods=['POST'])
def hook():
    
    if request.method == "POST": # and not "Yummietestbot" in request.json["message"]["from_user"]["username"]:
        
       #content = json.loads(request.get_data())# #WORKING
       
   
       chat_id=request.json["message"]["chat"]["id"]
       info=str(request.json["message"]["text"]).lower()
       #console.log(info)
       df_tutorial["vars"]=df_tutorial["Q"].apply(lambda string: is_similar(info, string))
       variants=df_temp.head(2).values
       bot.sendMessage(chat_id=chat_id, text=str(variants))
       
       
       return "ok"
