import telebot
import time
import json
import threading
from telebot import types
from googleapiclient.discovery import build
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import Table
from sqlalchemy import inspect
from datetime import datetime
from db_connections import *
import pymysql
import db_settings as ds
from services import json_string, json_string_2, json_string_3, video_links, sql_commands

BOT_TOKEN = '#' 
YOUTUBE_API_KEY = '#' # вставьте сюда ключ апи ютуба в3
#вставьте сюда токен своего бота
REFRESH_TIME = 1000 # время обновления с базой данных и ютубом в секундах 
ADMIN_IDS = [] # чат айди админов(можно посмотреть в базе данных)

bot = telebot.TeleBot(token=BOT_TOKEN)
############################################# DB ESTABLISHMENT ###################################
engine_wp = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(ds.USER_WP, ds.PASSWORD_WP, ds.HOST_WP, ds.DB_NAME_WP))
engine_bot = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(ds.USER_BOT, ds.PASSWORD_BOT, ds.HOST_BOT, ds.DB_NAME_BOT))
connection_wp = engine_wp.connect()
connection_bot = engine_bot.connect()
metadata = sqlalchemy.MetaData()
Base = declarative_base()
ins = inspect(engine_bot).get_table_names()
valid_symbols = ['+','0','1','2','3','4','5','6','7','8','9']

services_wordsnlink = json.loads(json_string_2)

faq_questions = json.loads(json_string_3)
  
last_questions = dict()



if not 'user' in ins:
  table = Table('user', metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name',String(20)),
    Column('last_name',String(20)),
    Column('username', String(15)),
    Column('registration_date',DateTime),
    Column('phone_number', String(15)))
  table.create(engine_bot)



if not 'message' in ins:
  table = Table('message', metadata,
    Column('id', Integer, primary_key=True, autoincrement = True),
    Column('sender_id',Integer),
    Column('date',DateTime),
    Column('text', String(5000)),
    Column('message_type', String(15)))
  table.create(engine_bot)
port_cats = {
"-- Автосигнализации --" :194,
"--Замки КПП и Капота--" : 1058,
"--Шумоизоляция--" : 193, 
"--Парковочные системы--":1060,
"--Автосвет--": 192,
"-- Иммобилайзеры --":195
 }
port_cats_inv = {
  '194' :"-- Автосигнализации --",
  '1058' : "--Замки КПП и Капота--",
  '193': "--Шумоизоляция--", 
  '1060':"--Парковочные системы--",
  '192': "--Автосвет--",
  '195':"-- Иммобилайзеры --"
 }
##############################  MARKUPS ############################

question1_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
item1 = types.KeyboardButton('Рекомендация')
item2 = types.KeyboardButton('Искал в Гугле')
item3 = types.KeyboardButton('Социальные сети')
item4 = types.KeyboardButton('Ютуб')
question1_markup.row(item1, item2)
question1_markup.row(item3, item4)

question3_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
item1 = types.KeyboardButton('Да')
item2 = types.KeyboardButton('Нет')
question3_markup.row(item1)
question3_markup.row(item2)

question2_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
item1 = types.KeyboardButton('1')
item2 = types.KeyboardButton('2')
item3 = types.KeyboardButton('3')
item4 = types.KeyboardButton('4')
item5 = types.KeyboardButton('5')
item6 = types.KeyboardButton('6')
item7 = types.KeyboardButton('7')
item8 = types.KeyboardButton('8')
item9 = types.KeyboardButton('9')
item10 = types.KeyboardButton('10')
question2_markup.row(item1, item2, item3,item4,item5)
question2_markup.row(item6, item7,item8,item9,item10)

start_markup = types.InlineKeyboardMarkup(row_width=1)
item1 = types.InlineKeyboardButton("--- Ответить на пару вопросов ---", callback_data='questions')
item2 = types.InlineKeyboardButton("--- НАЧНЁМ ---", callback_data='begin')
start_markup.add(item1, item2)

menu_markup = types.InlineKeyboardMarkup(row_width=1)
item2 = types.InlineKeyboardButton("Портфолио", callback_data='portfolio_menu')
item7 = types.InlineKeyboardButton("Тех поддержка", callback_data='FAQ')
item6 = types.InlineKeyboardButton("О компании", callback_data='info')
item5 = types.InlineKeyboardButton("Контакты  ", callback_data='contacts')
item1 = types.InlineKeyboardButton("Услуги", callback_data='services')
item3 = types.InlineKeyboardButton("Новости", callback_data='begin')
item4 = types.InlineKeyboardButton("Видео", callback_data='0_video')

menu_markup.add(item1, item2, item3, item4, item5, item6, item7)

services_markup = types.InlineKeyboardMarkup(row_width=1)   
services_data = json.loads(json_string)
for key in services_data.keys():
  data = '{}_service'.format(key)  
  item = types.InlineKeyboardButton(key, callback_data='{}_service'.format(key[:10]))
  services_markup.add(item)
item = types.InlineKeyboardButton('Меню', callback_data='menu')
services_markup.add(item)

portfolio_markup = types.InlineKeyboardMarkup(row_width=1)
services_data = json.loads(json_string)
for key in port_cats.keys():
  data = '0_port_cat{}'.format(port_cats[key])  
  item = types.InlineKeyboardButton(key, callback_data=data)
  portfolio_markup.add(item)
item = types.InlineKeyboardButton('Последние работы в портфолио', callback_data='0_portfolio')
portfolio_markup.add( item)
item = types.InlineKeyboardButton('Меню', callback_data='menu')
portfolio_markup.add( item)

faq_markup = types.InlineKeyboardMarkup(row_width=5)

item1 = types.InlineKeyboardButton("1", callback_data='faq_1')
item2 = types.InlineKeyboardButton("2", callback_data='faq_2')
item3 = types.InlineKeyboardButton("3", callback_data='faq_3')
item4 = types.InlineKeyboardButton("4", callback_data='faq_4')
item5 = types.InlineKeyboardButton("5", callback_data='faq_5')
item6 = types.InlineKeyboardButton("6", callback_data='faq_6')
item7 = types.InlineKeyboardButton("7", callback_data='faq_7')
item8 = types.InlineKeyboardButton("8", callback_data='faq_8')
item9 = types.InlineKeyboardButton("Задать вопрос", callback_data='calculate_')
item10 = types.InlineKeyboardButton("Меню", callback_data='menu')
faq_markup.add(item1, item2, item3, item4)
faq_markup.add(item5, item6, item7, item8)
faq_markup.row(item9)
faq_markup.row(item10)

info_markup = types.InlineKeyboardMarkup(row_width=1)
item3 = types.InlineKeyboardButton("Меню", callback_data='menu_i')
info_markup.add( item3)

faq_item_markup = types.InlineKeyboardMarkup(row_width=1)
item1 = types.InlineKeyboardButton("Задать вопрос", callback_data='calculate_')
item2 = types.InlineKeyboardButton("Назад", callback_data='FAQ')
item3 = types.InlineKeyboardButton("Меню", callback_data='menu')
faq_item_markup.add( item1, item2, item3)



def service_markup(service):
  markup = types.InlineKeyboardMarkup(row_width=1)
  item1 = types.InlineKeyboardButton("ПОДОБРАТЬ {} НА СВОЕ АВТО".format(services_wordsnlink[service][0]), callback_data='calculate_{}'.format(service[:10]))
  item2 = types.InlineKeyboardButton("УЗНАТЬ БОЛЬШЕ О {} НА YOUTUBE".format(services_wordsnlink[service][1]), url = services_wordsnlink[service][2])
  item3 = types.InlineKeyboardButton("СОЦИАЛЬНЫЕ СЕТИ", callback_data='contacts')
  item4 = types.InlineKeyboardButton("УЗНАТЬ БОЛЬШЕ О {} НА САЙТЕ".format(services_wordsnlink[service][1]), url = 'https://prime-technic.kiev.ua')
  item5 = types.InlineKeyboardButton("НАЗАД К УСЛУГАМ", callback_data='services')
  markup.add(item1, item2, item3, item4, item5)
  return markup
def article_markup_maker(article_id, size = 20):
  data1 = '{}_article'.format(str(int(article_id)-1))
  data2 = '{}_article'.format(str(int(article_id)+1))
  if int(article_id) < 1 :
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Далее 👉", callback_data=data2)
    markup.add(item1)
    return markup
  elif int(article_id) > size-2:
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("👈 Предыдущая", callback_data=data1)
    markup.add(item1)
    return markup
  markup = types.InlineKeyboardMarkup(row_width=2)  
  item1 = types.InlineKeyboardButton("👈 Предыдущая", callback_data=data1)
  item2 = types.InlineKeyboardButton("Далее 👉", callback_data=data2)
  markup.add(item1, item2)
  return markup

def portfolio_markup_maker(article_id, size = 20):
  data1 = '{}_portfolio'.format(str(int(article_id)-1))
  data2 = '{}_portfolio'.format(str(int(article_id)+1))
  if int(article_id) < 1 :
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Далее 👉", callback_data=data2)
    markup.add(item1)
    return markup
  elif int(article_id) > size-2:
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("👈 Предыдущая", callback_data=data1)
    markup.add(item1)
    return markup
  markup = types.InlineKeyboardMarkup(row_width=2)  
  item1 = types.InlineKeyboardButton("👈 Предыдущая", callback_data=data1)
  item2 = types.InlineKeyboardButton("Далее 👉", callback_data=data2)
  markup.add(item1, item2)
  return markup

def port_cat_markup_maker(article_id,cat, size = 5):
  data1 = '{}_port_cat{}'.format(str(int(article_id)-1), cat)
  data2 = '{}_port_cat{}'.format(str(int(article_id)+1), cat)
  if int(article_id) < 1 :
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Далее 👉", callback_data=data2)
    markup.add(item1)
    return markup
  elif int(article_id) > size-2:
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("👈 Предыдущая", callback_data=data1)
    markup.add(item1)
    return markup
  markup = types.InlineKeyboardMarkup(row_width=2)  
  item1 = types.InlineKeyboardButton("👈 Предыдущая", callback_data=data1)
  item2 = types.InlineKeyboardButton("Далее 👉", callback_data=data2)
  markup.add(item1, item2)
  return markup    

def video_markup_maker(article_id, size = len(video_links)):
  data1 = '{}_video'.format(str(int(article_id)-1))
  data2 = '{}_video'.format(str(int(article_id)+1))
  if int(article_id) < 1 :
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Далее 👉", callback_data=data2)
    markup.add(item1)
    return markup
  elif int(article_id) > size-2:
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("👈 Предыдущая", callback_data=data1)
    markup.add(item1)
    return markup
  markup = types.InlineKeyboardMarkup(row_width=2)  
  item1 = types.InlineKeyboardButton("👈 Предыдущая", callback_data=data1)
  item2 = types.InlineKeyboardButton("Далее 👉", callback_data=data2)
  markup.add(item1, item2)
  return markup  
############################################################ BOTs LOGIC ############################################

@bot.message_handler(commands=['start'])
def welcome(message):
  session_bot = sessionmaker(engine_bot)()
  new_user = session_bot.query(User).filter(User.id == message.from_user.id).first()
  if not new_user:
    new_user = User(id = message.from_user.id,  
      first_name = message.from_user.first_name,
      last_name = message.from_user.last_name,
      username = message.from_user.username,
      registration_date = datetime.now())
    session_bot.add(new_user)
    session_bot.commit()
  session_bot.close()      
  bot.send_message(message.chat.id, "<b>Приветствую, {0.first_name}, я Prime!\nBot для удобной навигации по услугам нашей компании “Prime Autotechnic”. Тут нет рекламы и только полезная информация.</b>".format(message.from_user), parse_mode = 'html')
  time.sleep(2)
  bot.send_message(message.chat.id, '<b>Ответь на пару вопросов для того чтобы наш сервис стал лучше или просто давай начнем!</b>', reply_markup=start_markup, parse_mode = 'html' )   

@bot.message_handler(commands=['help'])
def welcome(message):
  bot.send_message(message.chat.id, '<b>Просто нажимай кнопки меню!)</b>', reply_markup= info_markup, parse_mode='html' )

@bot.message_handler(commands=['menu'])
def welcome(message):
  bot.send_message(message.chat.id,'<b>============ МЕНЮ =======</b> ', reply_markup = menu_markup,parse_mode = 'html')     

@bot.message_handler(content_types=['text'])  
def default_response(message):
  session_bot = sessionmaker(engine_bot)()
  user = session_bot.query(User).filter(User.id == message.from_user.id).first()
  if not message.chat.id in last_questions.keys():
    last_questions[message.chat.id] = 'None'
  if last_questions[message.chat.id] == 'Откуда узнали о нас?':
    new_message = Message(sender_id = message.from_user.id, date = datetime.now(), text = message.text, message_type = 'q1' )
    bot.send_message(message.chat.id, 'Насколько довольны обслуживанием от 1 до 10?', reply_markup = question2_markup)
    for comm in sql_commands:
        if comm in new_message.text:
          new_message.text = 'SOMEONE TRIED TO BREAK INTO USING SQL INJECTION' 
    session_bot.add(new_message)
    session_bot.commit()
    last_questions[message.chat.id] = 'Насколько довольны обслуживанием от 1 до 10?'
  elif last_questions[message.chat.id] == 'Насколько довольны обслуживанием от 1 до 10?':
    new_message = Message(sender_id = message.from_user.id, date = datetime.now(), text = message.text, message_type = 'q2' )
    bot.send_message(message.chat.id, 'Что, на Ваш взгляд, необходимо нам улучшить в своей работе?', reply_markup = types.ForceReply(selective = False))  
    last_questions[message.chat.id] = 'Что, на Ваш взгляд, необходимо нам улучшить в своей работе?'
    for comm in sql_commands:
        if comm in new_message.text:
          new_message.text = 'SOMEONE TRIED TO BREAK INTO USING SQL INJECTION' 
    session_bot.add(new_message)
    session_bot.commit()    
  elif message.text == '--Меню--':
    bot.send_message(message.chat.id,'<b>============ МЕНЮ =======</b>', reply_markup = menu_markup, parse_mode = 'html')
  elif last_questions[message.chat.id] == 'Что, на Ваш взгляд, необходимо нам улучшить в своей работе?':
    new_message = Message(sender_id = message.from_user.id, date = datetime.now(), text = message.text, message_type = 'q4' )
    bot.send_message(message.chat.id, 'Будете ли рекомендовать друзьям?', reply_markup = question3_markup)
    try:
      for admin_id in ADMIN_IDS:
        bot.send_message(admin_id,'Что, на Ваш взгляд, необходимо нам улучшить в своей работе? \nСообщение от @{} \nНомер телефона: {} \nСодержание: \n{}'.format( message.from_user.username,user.phone_number,message.text))
    except:
      print('Something went wrong. Admins were not notified')    
    last_questions[message.chat.id] = 'Будете ли рекомендовать друзьям?'
    for comm in sql_commands:
        if comm in new_message.text:
          new_message.text = 'SOMEONE TRIED TO BREAK INTO USING SQL INJECTION' 
    session_bot.add(new_message)
    session_bot.commit()
  elif last_questions[message.chat.id] == 'Будете ли рекомендовать друзьям?':
    new_message = Message(sender_id = message.from_user.id, date = datetime.now(), text = message.text, message_type = 'q3' )
    if not user.phone_number:
      bot.send_message(message.chat.id,'Оставьте пожалуйста номер телефона, возможно руководство свяжется для выяснения деталей замечания если таковые имеются. Спасибо!', reply_markup = types.ReplyKeyboardRemove(selective=False)) 
      last_questions[message.chat.id] = 'Оставьте пожалуйста номер телефона, возможно руководство свяжется для выяснения деталей замечания если таковые имеются. Спасибо!'
    else:
      bot.send_message(message.chat.id,'Спасибо, ваш отзыв был записан!', reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True).row(types.KeyboardButton('--Меню--')) )
      bot.send_message(message.chat.id,'<b>============ МЕНЮ =======</b> ', reply_markup = menu_markup,parse_mode = 'html')
    for comm in sql_commands:
        if comm in new_message.text:
          new_message.text = 'SOMEONE TRIED TO BREAK INTO USING SQL INJECTION' 
    session_bot.add(new_message)
    session_bot.commit()     
  elif last_questions[message.chat.id] == 'Укажите ваш номер телефона' or last_questions[message.chat.id] == 'Оставьте пожалуйста номер телефона, возможно руководство свяжется для выяснения деталей замечания если таковые имеются. Спасибо!':
    valid = True
    if len(message.text) <= 7 or len(message.text) >= 12:
      valid = False 
    for symb in message.text:  
      if symb not in valid_symbols:
        valid = False
        break
    if valid:    
      user.phone_number = message.text
      session_bot.commit()
      if last_questions[message.chat.id] == 'Укажите ваш номер телефона':
        bot.send_message(message.chat.id, 'Какая услуга или вопрос Вас интересует?', reply_markup = types.ForceReply(selective= False))
        last_questions[message.chat.id] = 'Какая услуга или вопрос Вас интересует?'
      else:
        bot.send_message(message.chat.id,'Спасибо, ваш отзыв был записан!', reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True).row(types.KeyboardButton('--Меню--')) )
        bot.send_message(message.chat.id,'<b>============ МЕНЮ =======</b> ', reply_markup = menu_markup,parse_mode = 'html')
          
    else:
      if last_questions[message.chat.id] == 'Укажите ваш номер телефона':
        bot.send_message(message.chat.id, 'Укажите ваш номер телефона', reply_markup = portfolio_markup)
      else:
        bot.send_message(message.chat.id,'Спасибо, ваш отзыв был записан!', reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True).row(types.KeyboardButton('--Меню--')) )
        bot.send_message(message.chat.id,'<b>============ МЕНЮ =======</b> ', reply_markup = menu_markup,parse_mode = 'html')
        
  elif last_questions[message.chat.id] == 'Какая услуга или вопрос Вас интересует?':
    new_message = Message(sender_id = message.from_user.id, date = datetime.now(), text = message.text, message_type = 'question' )
    bot.send_message(message.chat.id, 'Ваше сообщение было успешно отправлено!', reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True).row(types.KeyboardButton('--Меню--')))
    try:
      for admin_id in ADMIN_IDS:
        bot.send_message(admin_id,'Какая услуга или вопрос Вас интересует? \nСообщение от @{} \nНомер телефона: {} \nСодержание: \n{}'.format( message.from_user.username,user.phone_number,message.text))
    except:
      print('Something went wrong. Admins were not notified')
    for comm in sql_commands:
      if comm in new_message.text:
        new_message.text = 'SOMEONE TRIED TO BREAK INTO USING SQL INJECTION' 
    session_bot.add(new_message)
    session_bot.commit()        
  session_bot.close()
     


@bot.callback_query_handler(func=lambda call: 'calculate_' in call.data)
def calc(call):
  markup = types.ForceReply(selective= False)
  session_bot = sessionmaker(engine_bot)()
  if session_bot.query(User).filter(User.id == call.from_user.id).first().phone_number:
    bot.send_message(call.message.chat.id, 'Какая услуга или вопрос Вас интересует?', reply_markup = types.ForceReply(selective= False))
    last_questions[call.message.chat.id] = 'Какая услуга или вопрос Вас интересует?'
  else:  
    bot.send_message(call.message.chat.id,'Укажите ваш номер телефона', reply_markup = markup)
    last_questions[call.message.chat.id] = 'Укажите ваш номер телефона'
  session_bot.close()
    
@bot.callback_query_handler(func=lambda call: 'begin' in call.data)
def begin(call):
  bot.send_message(call.message.chat.id, "Наши последние новости", reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True).row(types.KeyboardButton('--Меню--')))
  skip_num = 0  
  post = articles[skip_num]
  article_markup = article_markup_maker(skip_num)
  item3 = types.InlineKeyboardButton("ЧИТАТЬ", url='{}'.format(post[3]))
  item4 = types.InlineKeyboardButton("Меню", callback_data='menu')  
  article_markup.add(item3, item4)  
  bot.send_message(call.message.chat.id, "<b>{0}</b>\n{1}<a href='{2}'>.</a>".format(post[0],post[1][:-1],post[2]),parse_mode = 'html' ,reply_markup = article_markup)
        

#контанкты 
@bot.callback_query_handler(func=lambda call: 'contacts' in call.data)
def services_callback(call):
  bot.send_message(call.message.chat.id,"<a href = 'https://youtube.com/channel/UCwSYt0TIq9QixeVR7fZytFg?view_as=subscriber'>==========Youtube==========</a>\n<a href='https://www.instagram.com/prime_antiugon_kiev/'>==========Instagram==========</a>\n<a href = 'https://www.facebook.com/prime.s.lab/'>==========Facebook==========</a>\n<a>Оцените уровень и все преимущества нашего сервиса, который находится по адресу г. Киев, ул. Оранжерейная 3.</a>\n<a>ТЕЛ.: +38 (067) 617 65 04</a>", parse_mode='html', reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True).row(types.KeyboardButton('--Меню--')))
  bot.send_location(call.message.chat.id, latitude = 50.4663441, longitude = 30.4473086, reply_markup = portfolio_markup)
  
  
@bot.callback_query_handler(func=lambda call: 'services' in call.data)
def services_callback(call):
  bot.send_message(call.message.chat.id,'--Услуги--', reply_markup = services_markup)
  

@bot.callback_query_handler(func=lambda call: 'questions' in call.data)
def questions_callback(call):
  last_questions[call.message.chat.id] = 'Откуда узнали о нас?'
  bot.send_message(call.message.chat.id,'Откуда узнали о нас?', reply_markup = question1_markup)
    

@bot.callback_query_handler(func=lambda call: '_article' in call.data)
def article_callback(call):
  skip_num = int(call.data.replace('_article',''))  
  post = articles[skip_num]
  article_markup = article_markup_maker(skip_num)
  item3 = types.InlineKeyboardButton("ЧИТАТЬ", url='{}'.format(post[3]))
  item4 = types.InlineKeyboardButton("Меню", callback_data='menu')  
  article_markup.add(item3, item4)  
  bot.send_message(call.message.chat.id, "<b>{0}</b>\n{1}<a href='{2}'>.</a>".format(post[0],post[1][:-1],post[2]),parse_mode = 'html' ,reply_markup = article_markup) 
  bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: 'portfolio_menu' in call.data)
def menu_callback(call):
  bot.send_message(call.message.chat.id,'<b> Выберите категорию услуг которая вас интересует </b> ', reply_markup = portfolio_markup,parse_mode = 'html')

@bot.callback_query_handler(func=lambda call: '_portfolio' in call.data)
def portfolio_callback(call):
  skip_num = int(call.data.replace('_portfolio',''))  
  post = portfolio_latest_articles[skip_num] 
  article_markup = portfolio_markup_maker(skip_num)
  item3 = types.InlineKeyboardButton("ЧИТАТЬ", url='{}'.format(post[3]))
  item4 = types.InlineKeyboardButton("Назад", callback_data='portfolio_menu')  
  article_markup.add(item3, item4)  
  bot.send_message(call.message.chat.id, "<b>{0}</b>\n{1}<a href='{2}'>.</a>".format(post[0],post[1][:-1],post[2]),parse_mode = 'html' ,reply_markup = article_markup) 
  bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

@bot.callback_query_handler(func=lambda call: '_port_cat' in call.data)
def port_cat_callback(call):
  skip_num = int(call.data.split('_port_cat')[0])
  cat = call.data.split('_port_cat')[1]
  size = len(portfolio_articles[port_cats_inv[cat]])
  post = []
  if size > 1:
    post = portfolio_articles[port_cats_inv[cat]][skip_num]
    article_markup = port_cat_markup_maker(skip_num,cat,size)
  elif size == 0:
    post = ['Пока нет работ из этой категории','########','https://prime-technic.kiev.ua/','https://prime-technic.kiev.ua/']
    article_markup = types.InlineKeyboardMarkup(row_width=1)  
  else:
    post = portfolio_articles[port_cats_inv[cat]][skip_num]
    article_markup = types.InlineKeyboardMarkup(row_width=1) 
  item3 = types.InlineKeyboardButton("ЧИТАТЬ", url='{}'.format(post[3]))
  item4 = types.InlineKeyboardButton("Назад", callback_data='portfolio_menu')  
  article_markup.add(item3, item4)  
  bot.send_message(call.message.chat.id, "<b>{0}</b>\n{1}<a href='{2}'>.</a>".format(post[0],post[1][:-1],post[2]),parse_mode = 'html' ,reply_markup = article_markup) 
  bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)  

@bot.callback_query_handler(func=lambda call: '_video' in call.data)
def article_callback(call):
  skip_num = int(call.data.replace('_video',''))  
  video_markup = video_markup_maker(skip_num)
  item4 = types.InlineKeyboardButton("Меню", callback_data='menu')  
  video_markup.add(item4)  
  bot.send_message(call.message.chat.id, video_links[skip_num] ,reply_markup = video_markup) 
  bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)    

#Тех поддержка(вопросы)
@bot.callback_query_handler(func=lambda call: 'FAQ' in call.data)
def faq_callback(call):
  bot.send_message(call.message.chat.id,"Вопросы по какой теме вас интересуют:\n 1. Защита авто от угона \n 2. Бронипленка \n 3. Карбон \n 4. Шумоизоляция \n 5. Парковочные системы \n 6. Мультимедиа, регистраторы и акустика\n 7. Автосвет \n 8. Покраска, полировка \n 9. Задать вопрос \n 10.Вернутся в меню", reply_markup = faq_markup)
  

@bot.callback_query_handler(func=lambda call: 'faq_' in call.data)
def faq_callback(call):
  bot.send_message(call.message.chat.id,faq_questions[call.data.replace('faq_','')], parse_mode = 'html',reply_markup = faq_item_markup)
  

#Тут информация о компании
@bot.callback_query_handler(func=lambda call: 'info' in call.data)
def infp_callback(call):
  video = open('media/info.MP4', 'rb')  
  bot.send_video(call.message.chat.id, video)
  bot.send_message(call.message.chat.id,'Мы – это современная команда, удачно соединившая в себе молодое руководство и сотрудников с опытным техническим персоналом. Находимся в постоянном развитии с целью сделать Вашу машину совершеннее. В нашей деятельности мы практикуем прогрессивный подход к монтажу, обслуживанию и ремонту дополнительного оборудования для машин. Он основан на индивидуальном подходе к решению задач клиента с целью оптимизации его финансовых затрат.', reply_markup = info_markup)


@bot.callback_query_handler(func=lambda call: 'menu' in call.data)
def menu_callback(call):
  bot.send_message(call.message.chat.id,'<b>============ МЕНЮ =======</b> ', reply_markup = menu_markup,parse_mode = 'html')
   

@bot.callback_query_handler(func=lambda call:'_service' in call.data)
def service_callback(call):
  service_name = call.data.replace('_service', '')
  for name in services_data.keys():
    if service_name in name:
      service_name = name
      break
  bot.send_message(call.message.chat.id, "<b>{}</b>".format(service_name), parse_mode = 'html')
  try:
    photo = open('media/{}.jpg'.format(service_name), 'rb')
    bot.send_photo(call.message.chat.id, photo)
  except:
    pass  
  bot.send_message(call.message.chat.id, "{}".format(services_data[service_name]), parse_mode = 'html', reply_markup = service_markup(service_name))        

############################################### UPDATING DATA ###################################################

def get_latest_posts(skip_number = 20):
  articles1 = []
  session = sessionmaker(bind=engine_wp)()
  post_query = session.query(Post).order_by(Post.id.desc()).all() 
  counter = 0 
  for _row in post_query:
    if counter < skip_number:
      if _row.ping_status == 'open' and _row.post_status == 'publish' and _row.post_type =='post':
        image_link = '#'
        try:  
          pic_query = session.query(PostMeta).filter(PostMeta.post_id == _row.id)  

          pic_id = 0
          for pic in pic_query:
            if pic.meta_key == '_thumbnail_id':
              pic_id = pic.meta_value
              break
          image_link = session.query(Post).filter(Post.id == pic_id).first().guid
        except:
          continue    
        articles1.append([_row.post_title, _row.post_excerpt, image_link, _row.guid])
        counter += 1
  session.close()      
  return articles1

def get_portfolio_latest_articles(skip_number = 20):
  articles1 = []
  session = sessionmaker(bind=engine_wp)()
  post_query = session.query(Post).order_by(Post.id.desc()).all() 
  counter = 0 
  for _row in post_query:
    if counter < skip_number:
      if _row.ping_status == 'open' and _row.post_status == 'publish' and _row.post_type =='post':
        in_portfolio = False
        try:
          post_terms = session.query(TermRelationship).filter(TermRelationship.object_id == _row.id)
          for term in post_terms:
            if term.term_taxonomy_id == 27:
              in_portfolio = True
        except:
          pass
        if in_portfolio:        
          image_link = '#'
          try:  
            pic_query = session.query(PostMeta).filter(PostMeta.post_id == _row.id)  

            pic_id = 0
            for pic in pic_query:
              if pic.meta_key == '_thumbnail_id':
                pic_id = pic.meta_value
                break
            image_link = session.query(Post).filter(Post.id == pic_id).first().guid
          except:
            continue    
          articles1.append([_row.post_title, _row.post_excerpt, image_link, _row.guid])
          counter += 1
  session.close()      
  return articles1  

def get_portfolio_articles(port_cats, skip_number = 5):
  articles1 = {}
  session = sessionmaker(bind=engine_wp)()
  post_query = session.query(Post).order_by(Post.id.desc()).all() 
  for cat in  port_cats.keys():
    counter = 0
    articles1[cat] = []
    posts_filt_id = []
    #try:
    post_terms = session.query(TermRelationship).filter(TermRelationship.term_taxonomy_id == port_cats[cat])
    for term in post_terms: 
      posts_filt_id.insert(0,term.object_id)       
    #except:
     # pass
    for  lid  in posts_filt_id:
      if counter < skip_number:       
        image_link = '#'
        try:
          _row = session.query(Post).filter(Post.id == lid).first()
          if _row.ping_status == 'open' and _row.post_status == 'publish' and _row.post_type =='post':
            pic_query = session.query(PostMeta).filter(PostMeta.post_id == _row.id)  
            pic_id = 0
            for pic in pic_query:
              if pic.meta_key == '_thumbnail_id':
                pic_id = pic.meta_value
                break
            image_link = session.query(Post).filter(Post.id == pic_id).first().guid
            articles1[cat].append([_row.post_title, _row.post_excerpt, image_link, _row.guid])
            counter += 1
        except:
          continue            
      else:
        break  
  session.close()      
  return articles1   
       
  


def time_counter(REFRESH_TIME):
  while True: 
    try:
      global articles
      global last_article
      articles = get_latest_posts()
      try:
        if last_article != articles[0]:
          session_bot = sessionmaker(engine_bot)()
          users = session_bot.query(User).all()
          post = articles[0]
          article_markup = article_markup_maker(0)
          item3 = types.InlineKeyboardButton("ЧИТАТЬ", url='{}'.format(post[3]))
          item4 = types.InlineKeyboardButton("Меню", callback_data='menu')  
          article_markup.add(item3, item4)
          for user in users:
            try:
              bot.send_message(user.id,'Новая новость!')  
              bot.send_message(user.id, "<b>{0}</b>\n{1}<a href='{2}'>.</a>".format(post[0],post[1][:-1],post[2]),parse_mode = 'html' ,reply_markup = article_markup)
            except:
              print("Can't send message to user with id: {}".format(user.id))         
          last_article = articles[0]
      except:
        last_article = articles[0]    
      print('News were updated')  
    except:
      print("Something went wrong, news couldn't be updated")
    try:
      global portfolio_latest_articles
      global portfolio_articles
      portfolio_articles = get_portfolio_articles(port_cats)
      portfolio_latest_articles = get_portfolio_latest_articles()
      print('Portfolio was updated')
    except:
      print("Something went wrong, portfolio couldn't be updated")  
    try:
      youtube = build('youtube','v3', developerKey = YOUTUBE_API_KEY)    
      res = youtube.playlistItems().list(part = 'contentDetails', playlistId = 'UUwSYt0TIq9QixeVR7fZytFg', maxResults = 10).execute()
      global video_links
      video_links = []
      for item in res['items']:
        video_links.append('https://www.youtube.com/watch?v={}'.format(item['contentDetails']['videoId']))
      print('Youtube links were updated')  
    except:
      print("Something went wrong, youtube links couldn't be updated")   
    time.sleep(REFRESH_TIME)  

update_articles = threading.Thread(target = time_counter,args=(REFRESH_TIME,))
update_articles.start()


while True:
  try:
    bot.polling()        
  except Exception:
    time.sleep(15)          