from flask import Flask, request
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

#f=open(os.path.join("data", "df_all_articles.csv"))
#data=open("df_all_articles.csv")
#li = f.read()#.split('\n')
#df_articles=pd.read_csv(StringIO(li))
#df_tutorial = pd.read_csv("FV_tutorial.csv")
#df_articles = pd.DataFrame(df_list, columns=["Q", "link", "category"])

df_articles=pd.read_csv(os.path.join("data", "df_all_articles.csv"))
df_tutorial=pd.read_csv(os.path.join("data", "fv_tutorial.csv"))

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
       
       
       if "start" in info:
           bot.sendMessage(chat_id=chat_id, text=greet_text)
           bot.sendMessage(chat_id, "Пожалуйста, выбери в синем меню, где мне поискать!")
           msg_counter+=1
       if any(item in info for item in ["tutorial", "article", "tag"]):
           GLOBAL_SEARCH+=info
           bot.sendMessage(chat_id, text="Введи, пожалуйста, ключевые слова или вопрос.")
            
        
       if GLOBAL_SEARCH=="tutorial":
           df_tutorial["vars"]=df_tutorial["Q"].apply(lambda string: is_similar(info, string))
           df_temp=df_tutorial.sort_values("vars", ascending=[False]).head(max(5, df_tutorial.index[df_tutorial.vars==0][0]))
           variants=df_temp.values
        #forming link from ttorial
           for var in variants:
               bot.sendMessage(chat_id=chat_id,
                                    text=var[0]+"\n"+
                                    f"http://cit.bsau.ru/netcat_files/File/CIT/manuals/Flow_Vision.pdf#page={var[1]}",
                                    disable_web_page_preview=True)
       
       if GLOBAL_SEARCH=="article":
           df_articles["vars"]=df_articles["Q"].apply(lambda string: is_similar(info, string))
           df_temp=df_article.sort_values("vars", ascending=[False]).head(max(5, df_article.index[df_article.vars==0][0]))
           variants=df_temp.values
        #forming link from ttorial
           for var in variants:
               bot.sendMessage(chat_id=chat_id,
                                    text=var[0]+"\n"+
                                    str(var[1]))
    
       if GLOBAL_SEARCH=="tag":
           df_temp=df_article[df_article["category"]==info[:-1]]
           variants=df_temp.values
           for var in variants:
               bot.sendMessage(chat_id=chat_id,
                                    text=var[2]+"\n"+
                                    str(var[1]))
       
       
       #chat_id="1093497662"# msg.sender_chat["username"]
       #bot.sendMessage(chat_id=chat_id, text=info)
    return "ok"
