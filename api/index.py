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
global KEYWORDS
df_articles=pd.read_csv(os.path.join("data", "df_all_articles.csv"))
df_tutorial=pd.read_csv(os.path.join("data", "fv_tutorial.csv"))
df_tags=pd.read_csv(os.path.join("data", "tags_df.csv"))
df_articles.apply(lambda x: x.astype(str).str.lower())
df_tutorial.apply(lambda x: x.astype(str).str.lower())

GLOBAL_SEARCH=None
KEYWORDS=None


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
    df_articles["vars"]=df_articles["Q"].apply(lambda string: is_similar("турбина", string))
    df_temp=df_articles.sort_values("vars", ascending=[False]).head(max(7, df_articles.index[df_articles.vars==0][0]))
    df_temp=df_temp.drop_duplicates()
    variants=df_temp.values
    bot.sendMessage(chat_id="1093497662", text=str(variants))
    
    
  

@app.route("/"+TOKEN, methods=['POST'])
def hook():
    global df_articles
    global df_tutorial
    global GLOBAL_SEARCH
    global KEYWORDS
    CHAT_ID=None      
           
    
    if request.method == "POST":
       # and not "Yummietestbot" in request.json["message"]["from_user"]["username"]:
       
       content = json.loads(request.get_data())# #WORKING
       chat_id=content["message"]["chat"]["id"]
       CHAT_ID=chat_id
       info=str(content["message"]["text"]).lower()
        
       #if GLOBAL_SEARCH is not None and KEYWORDS is not None:
           # testing()
          #search()        
           
                 
       if "help" in info:
           bot.sendMessage(chat_id, text="Привет, я бот-простоо поиска. 1 ВЫБЕРИ В СИНЕМ МЕНЮ, ГДЕ МНЕ ИСКАТЬ \n 2. ВВЕДИ КЛЮЧЕВЫЕ СЛОВА \n\
           Я ищу в туториале, на сайте по названиям статей или на сайте по тэгам и темам") #TEST
            
       elif "alltags" in info:
           variants=df_tags.values
           for var in variants:
               bot.sendMessage(chat_id=chat_id,
                                   text=var[0]+"\n"+var[1])
          
            
            
       elif info in ["/tutorial", "/articles", "/tags"]: 
        #and content["message"]["from"]["is_bot"]==False: #and #not any(info[1:] in s for s in ["tutorial", "article", "tag", "help"]): #content["message"]["entities"]["type"]!="bot_command" and GLOBAL_SEARCH is not None: 
            GLOBAL_SEARCH = info[1:]
            #search()
            #ONE MORE TEST
            #bot.sendMessage(chat_id=chat_id, text=str([GLOBAL_SEARCH, KEYWORDS])) #WORKING #################################
       else:
            KEYWORDS=info
            if GLOBAL_SEARCH == "tutorial":
                df_tutorial["vars"]=df_tutorial["Q"].apply(lambda string: is_similar(KEYWORDS, string))
                df_temp=df_tutorial.sort_values("vars", ascending=[False]).head(max(7, df_tutorial.index[df_tutorial.vars==0][0]))
                df_temp=df_temp.drop_duplicates()
                if df_temp.head(3)==df_tutorial.head(3):
                    bot.sendMessage(chat_id=chat_id, 
                                   text="Ничего не нашлось! Переформулируйте, пожалуйста!")
                variants=df_temp.values
                #GLOBAL_SEARCH = None
                #KEYWORDS = None
        #forming link from ttorial
                for var in variants:
                    bot.sendMessage(chat_id=chat_id, 
                                   text=var[0]+"\n"+
                                   f"http://cit.bsau.ru/netcat_files/File/CIT/manuals/Flow_Vision.pdf#page={var[1]}",
                                   disable_web_page_preview=False)
            elif GLOBAL_SEARCH == "articles":
                df_articles["vars"]=df_articles["Q"].apply(lambda string: is_similar(KEYWORDS, string))
                df_temp=df_articles.sort_values("vars", ascending=[False]).head(max(5, df_articles.index[df_articles.vars==0][0]))
                df_temp=df_temp.drop_duplicates()
                if df_temp.head(3)==df_articles.head(3):
                    bot.sendMessage(chat_id=chat_id, 
                                   text="Ничего не нашлось! Переформулируйте, пожалуйста!")
                variants=df_temp.values
            #GLOBAL_SEARCH = Npne
            #KEYWORDS = None
        #forming link from ttorial
                for var in variants:
                    bot.sendMessage(chat_id=chat_id,
                                   text=var[0]+"\n"+str(var[1]))
            elif GLOBAL_SEARCH == "tags":
                df_temp=df_tags[df_tags["tag"]==KEYWORDS[:-1]]
                variants=df_temp.values
                if not variants:
                    bot.sendMessage(chat_id=chat_id, 
                                   text="Ничего не нашлось! Переформулируйте, пожалуйста!")
                    
                #GLOBAL_SEARCH = None
                #KEYWORDS = None
                for var in variants:
                    bot.sendMessage(chat_id=chat_id,
                                   text=var[0]+"\n"+
                                   str(var[1]))
                    
                 
            
           
        

       return "ok"
