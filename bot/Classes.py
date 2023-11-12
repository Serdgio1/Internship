import telebot
from telebot import types

class Button:
    def Add_button(self,text,callback):
        self.add(types.InlineKeyboardButton(text,callback_data=callback))

class Chats:
    def __init__(self, chat):
        l = list(chat.split())
        self.id = l[0]
        self.n = l[1]
        self.c = l[2]