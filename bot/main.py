import telebot
from telebot import types
import Classes
from Classes import Button

superAdmin = '5034471316' # Имя суперадмина

# Определяющие переменные
send_all = False
sen_paral = False
data = ''
id_m = 0
ex = list()
admin_dict = list()

API_TOKEN = '6829285336:AAE8d821gRiJJJOw6OFwrlhCpKMkTMSQXfU' #Токен

bot = telebot.TeleBot(API_TOKEN) # Переменная для обращения к боту


# Функия создания линейной разметки
def Markup():
    markup = types.InlineKeyboardMarkup()
    return markup

# Проверка
def Check(message):
    file_admins = open('admin.txt', 'r+', encoding='utf-8')
    lines = file_admins.readlines()
    for line in lines:
        admin_dict.append(line)
    if message.from_user.id==int(superAdmin) or (message.chat.username in admin_dict):
        return True
    return False

# Функция для нахождения чата
def Find_all(key):
    id = ''
    id_dict = list()
    f = open('chats.txt','r+', encoding='utf-8')
    lines = f.readlines()
    for number, line in enumerate(lines,1):
        if key in line:
            ex.append(line)
    f.close()
    for i in range(0,len(ex)):
        for k in ex[i]:
            if k==' ':
                id_dict.append(id)
                id = ''
                break
            id+=k
    ex.clear()
    if len(id_dict)!=0:
        return id_dict
    return 1


# Информация о чате
@bot.message_handler(commands=['info'])
def Info(message):
    bot.send_message(superAdmin,f'{message.chat.id} {message.chat.title}')

# Добавить чат
@bot.message_handler(commands=['add_chat'])
def Add_chat(message):
    if Check(message):
        chat = Classes.Chats(message.text[10::])
        with open('chats.txt','a+', encoding='utf-8') as file_chats:
            file_chats.write(chat.id + ' ' + chat.n + ' ' + chat.c + '\n')
        bot.send_message(message.chat.id,'done')

# Добавить админа
@bot.message_handler(commands=['add_admin'])
def Add_admin(message):
    if Check(message):
        with open('admin.txt', 'a+', encoding='utf-8') as file_admin:
            file_admin.write(message.text[11::]+'\n')
        bot.send_message(message.chat.id, 'done')

# Старт бота
@bot.message_handler(commands=['send', 'start'])
def send_welcome(message):
    global mesagedel
    if Check(message):
        markup = Markup()
        Button.Add_button(markup,"Всем",'all')
        Button.Add_button(markup, "Параллели", 'paral')
        mesagedel = bot.send_message(message.chat.id, "Кому хотите отправить сообщение? \nЕсли вас интересует инструкция по боту напишите /help", reply_markup=markup)

# Информация о боте
@bot.message_handler(commands=['help'])
def Help(message):
    if Check(message):
        bot.send_message(message.chat.id,"Поздравляю вы администратор! Вот функции для управления ботом\n /add_chat - добавляет чат с классом вот пример(/add_chat 123 name 11.3)\n"
                                         "/add_admin добавляет администратора(/add_admin nickname)\n /send или /start открывает меню отправки сообщения\n Если надо отправить всем, то при добавлении чата в имени пропишите all")

# Подверждение
@bot.callback_query_handler(func=lambda callback: callback.data == 'all')
def callback_paral(callback):
    global send_all
    bot.delete_message(callback.message.chat.id, mesagedel.id)
    bot.send_message(callback.message.chat.id,'Отправь сообщение для ВСЕХ чатов:')
    send_all=True

# Выбор параллели
@bot.callback_query_handler(func=lambda callback: callback.data == "paral")
def callback_paral(callback):
    global mesagedel
    bot.delete_message(callback.message.chat.id,mesagedel.id)
    markup = Markup()
    Button.Add_button(markup, "5 классы", '5')
    Button.Add_button(markup, "6 классы", '6')
    Button.Add_button(markup,"7 классы",'7')
    Button.Add_button(markup, "8 классы", '8')
    Button.Add_button(markup, "9 классы", '9')
    Button.Add_button(markup, "10 классы", '10')
    Button.Add_button(markup, "11 классы", '11')
    mesagedel = bot.send_message(callback.message.chat.id, "Кому хотите отправить сообщение? ", reply_markup=markup)


# Отправка для конкретной параллели
@bot.callback_query_handler(func=lambda callback: callback.data == '5' or callback.data == '6' or callback.data == '7' or callback.data == '8' or callback.data == '9' or callback.data == '10' or callback.data == '11')
def callback_paral(callback):
    global sen_paral, data
    data = callback.data
    bot.delete_message(callback.message.chat.id, mesagedel.id)
    bot.send_message(callback.message.chat.id, f'Отправь сообщение для {callback.data} классов:')
    sen_paral = True

# Прием текстового сообщения
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global send_all, data, sen_paral, id_m
    if send_all:
        markup = Markup()
        Button.Add_button(markup,'ОТПРАВИТЬ','s_all')
        bot.send_message(message.chat.id, "Точно отправить?", reply_markup=markup)
        id_m = message.id
        send_all=False
    if sen_paral:
        markup = Markup()
        Button.Add_button(markup, 'ОТПРАВИТЬ', data+'.')
        bot.send_message(message.chat.id, "Точно отправить?", reply_markup=markup)
        id_m = message.id
        sen_paral = False
    with open('ivents.txt','r+', encoding='utf-8') as f: # добавить чат в список по сообщению
        lines = f.readlines()
        key = (str(message.chat.id) + ' ' + str(message.chat.title)+'\n')
        if key not in lines: # проверка если чат уже добавлен
            f.write(key)
            bot.send_message(superAdmin,'new chat add')


# Попытка отправить всем добавленным чатам
@bot.callback_query_handler(func=lambda callback: callback.data == 's_all')
def callback_paral(callback):
    global id_m
    try:
        id = Find_all('all')
        for i in id:
            bot.copy_message(int(i), callback.message.chat.id, id_m)
        id.clear()
    except:
        bot.send_message(callback.message.chat.id,'Такого чата не существует')

# Попытка отправить опрделенной параллели
@bot.callback_query_handler(func=lambda callback: callback.data == data+'.')
def callback_paral(callback):
    global  data, id_m
    try:
        id = Find_all(data + '.')
        for i in id:
            bot.copy_message(int(i), callback.message.chat.id, id_m)
        data = ''
    except:
        bot.send_message(callback.message.chat.id,'Такого чата не существует')


bot.infinity_polling(none_stop = True)