import telebot
from telebot import types
import sqlite3
from time import sleep
admins = [] # Тут юзер-айди
bd = sqlite3.connect('base.db')
cursor = bd.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users(status INT , id_user BIGINT PRIMARY KEY)')
cursor.close()
bd.close()
bot = telebot.TeleBot('') # Тут суется токег
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Наш канал',url='') #Ссылка на канал
    markup.add(btn1)
    user_id = message.chat.id
    chatid = '' #Айди канала
    if 'member' == bot.get_chat_member(chatid,user_id).status or 'creator' == bot.get_chat_member(chatid,user_id).status or 'administrator' == bot.get_chat_member(chatid,user_id).status:
        bot.send_message(message.chat.id,'Привет, данный бот поможет тебе проверить человека на скам!\n⚡️Спасибо, что выбрали именно нашего бота для проверки скамеров🌟\nТак же вы можете слить своего обидчика в нашу предложку: Ее нет лол)\n🤝Данный бот может использоваться в вашей группе, чтобы другие люди могли проверить человека на скам!👨\n‍💻Если вы хотите стать гарантом базы, то эт тест база\n Подробнее команды в /help')
    else:
        bot.send_message(message.chat.id,'Ээээ а на канал кто подпишется?',reply_markup=markup)
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,'▶️ СПИСОК КОМАНД ДОСТУПНЫЙ ОБЫЧНЫМ ЮЗЕРАМ:\n/start - запуск бота \n /check  - проверет пользователя на доверие \n /help - выдаст список команд \n⚙️ СПИСОК КОМАНД ДОСТУПНЫЙ ДЛЯ АДМИНОВ:\n /add - добавит юзера в базу \n /addad - добавит юзера в админы \n /del - удалит из базы данных пользователя\n /delad - удалить админа (только создатель)')
@bot.message_handler(commands=['add'])
def add_base(message):
    if message.from_user.id in admins:
        a12=bot.send_message(message.chat.id,'Напиши айди')
        bot.register_next_step_handler(a12,add)
    else:
        bot.send_message(message.chat.id, '❎ Недостаточно прав для данной команды.')
def add(message):
    global ids
    ids = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1= types.InlineKeyboardButton('🥉Гарант🥉')
    btn2= types.InlineKeyboardButton('❌Скам❌')
    btn3 = types.InlineKeyboardButton('🍩Администратор🍩')
    markup.add(btn1,btn2)
    markup.add(btn3)
    changer = bot.send_message(message.chat.id, 'Заносим как?',reply_markup=markup)
    bot.register_next_step_handler(changer,vnos)
def vnos(message):
    global status1
    if message.text == '🥉Гарант🥉':
        status1 = 1
    elif message.text == '❌Скам❌':
        status1 = 2
    elif message.text == '🍩Администратор🍩':
        status1 = 3
    try:
        bd = sqlite3.connect('base.db')
        cursor = bd.cursor()
        ids1 = int(ids)
        cursor.execute('INSERT INTO users VALUES(?,?);',(status1,ids1))
        bd.commit()
        cursor.close()
        bd.close()
        bot.send_message(message.chat.id, '✅ Пользователь добавлен в базу.')
    except:
        bot.send_message(message.chat.id,'❎ Вы не правильно указали ID пользователя')
@bot.message_handler(commands=['addad'])
def add_base(message):
    if message.from_user.id in admins:
        adminka=bot.send_message(message.chat.id,'Напиши айди')
        bot.register_next_step_handler(adminka,add_base1)
    else:
        bot.send_message(message.chat.id, '❎ Недостаточно прав для данной команды.')
def add_base1(message):
    try:
        b1=int(message.text)
        admins.append(b1)
        bot.send_message(message.chat.id, f' Пользователю с id {b1} выданы права админа.')
    except:
        bot.send_message(message.chat.id,'❎ Вы не правильно указали ID пользователя')
@bot.message_handler(commands=['check'])
def check1(message):
    check2 = bot.send_message(message.chat.id, 'Напиши айди')
    bot.register_next_step_handler(check2, check3)
def check3(message):
    try:
        id_check = int(message.text)
        old_message = bot.send_message(message.chat.id, '🕰 Ищу в базе данных...')
        if id_check == 123456: #Вместо 123456 юзер айди
            bot.edit_message_text(f'🆔ID:{id_check}\n👑Находится в базе как Владелец👑', message.chat.id,old_message.message_id)
        else:
            bd = sqlite3.connect('base.db')
            cursor = bd.cursor()
            cursor.execute(f"SELECT * FROM users WHERE id_user ={id_check} ")
            bd.commit()
            check = cursor.fetchone()
            cursor.close()
            bd.close()
            sleep(2)
            if check:
                a7=check[0]
                if a7 == 3:
                    bot.edit_message_text(f'🆔ID:{id_check}\n🍩Находится в базе как Администратор🍩', message.chat.id,old_message.message_id)
                elif a7 == 2:
                    bot.edit_message_text(f'🆔ID:{id_check}\n❌Находится в базе как скамер!❌',message.chat.id,old_message.message_id)
                elif a7 == 1:
                    bot.edit_message_text(f'🆔ID:{id_check}\n✅Находится в базе как 🥉Гарант ', message.chat.id, old_message.message_id)
            else:
                bot.edit_message_text(f'🆔ID:{id_check}\n🌌Является обычным пользователем.', message.chat.id, old_message.message_id)
    except:
        bot.send_message(message.chat.id, '❎ Вы не правильно указали ID пользователя')
@bot.message_handler(commands=['del'])
def delete1(message):
    if message.from_user.id in admins:
        da1 = bot.send_message(message.chat.id, 'Напиши айди')
        bot.register_next_step_handler(da1, d2)
    else:
        bot.send_message(message.chat.id, '❎ Недостаточно прав для данной команды.')
def d2(message):
    try:
        ide=int(message.text)
        bd = sqlite3.connect('base.db')
        cursor = bd.cursor()
        cursor.execute(f"DELETE FROM users WHERE id_user = {ide}")
        bd.commit()
        cursor.close()
        bd.close()
        bot.send_message(message.chat.id,'✅ Удален с базы данных.')
    except:
        bot.send_message(message.chat.id, '❎ Вы не правильно указали ID пользователя')
@bot.message_handler(commands=['delad'])
def delete_admin(message):
    if message.from_user.id == 12345 : # Вместо 12345 свой юзер айди
        da11 = bot.send_message(message.chat.id, 'Напиши айди')
        bot.register_next_step_handler(da11, da22)
    else:
        bot.send_message(message.chat.id, '❎ Недостаточно прав для данной команды.')
def da22(message):
    try:
        ide1=int(message.text)
        admins.remove(ide1)
        bot.send_message(message.chat.id,'✅ Права админа сняты')
    except:
        bot.send_message(message.chat.id, '❎ Вы не правильно указали ID пользователя/Нету в админах')
bot.infinity_polling()