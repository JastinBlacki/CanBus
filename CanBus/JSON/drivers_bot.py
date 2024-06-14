import telebot
from telebot import types
from functions_for_json import *

token = '6803273240:AAHl3sx7ycEbobOGigUVLcp7L_uNOxnktXY'
bot = telebot.TeleBot(token)

dict_def = {"ID_defect": None, 'car_id': None, 'driver_id': None, 'Type1': None, 'Type2': None, 'describe': None}


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Здравствуй,  напиши свой номер телефона в виде - '+79999999999' для регистрации")
    bot.register_next_step_handler(message, is_registered)


def is_registered(message):
    chat_id = message.chat.id
    registered_drivers = registered_users_login('Водитель')
    if str(message.text) in registered_drivers:
        bot.send_message(chat_id, "Введите пароль")
        id_driver = get_id_driver_phone(message.text)[0]
        dict_def.update({"driver_id": id_driver}) # После того как пользователь зарегался создется словарь со всей его инфой
        dict_def.update({"car_id": get_car(id_driver, "Driver")[0]})
        dict_def.update({"ID_defect": get_id_df()})
        bot.register_next_step_handler(message, pass_login_drivers)
    else:
        bot.send_message(chat_id, "Вашего номера телефона не найдено в базе данных.")


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Добавить поломку (введите /add)")


def pass_login_drivers(message):
    password_drivers = registered_users_password("Водитель")
    if str(message.text) in password_drivers:
        bot.send_message(message.chat.id, 'Вы успешно вошли в аккаунт')
        bot.send_message(message.chat.id, "Для просмотра всех функций введите /help")


@bot.message_handler(commands=['add'])
def message_add_def(message):
    if dict_def["driver_id"] is None:
        markup1 = types.InlineKeyboardMarkup()
        markup1.add(types.InlineKeyboardButton('Зарегистрироваться', callback_data='reg'))
        bot.send_message(message.chat.id, 'Вы не зарегистрировались', reply_markup=markup1, parse_mode='html')
    else:
        markup1 = types.InlineKeyboardMarkup()
        markup1.add(types.InlineKeyboardButton('Механический', callback_data='mechanica'))
        markup1.add(types.InlineKeyboardButton('Электрический', callback_data='electric'))
        bot.send_message(message.chat.id, 'Выберите тип поломки', reply_markup=markup1, parse_mode='html')


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    chat_id = callback.message.chat.id
    call_funk = callback.data
    message = callback.message
    deleter(message)
    if call_funk == 'mechanica':
        mechanica(message) # если поломка механическая
    elif call_funk == 'electric':
        electric(message) # если поломка электрическая
    elif call_funk[:8] == 'comm_def':
        func_type2(message, call_funk[8:]) # подтипы поломок (система охлаждения и т.п.)
    elif 'reg':
        start_message(message)


@bot.message_handler(content_types=['text'])
def mechanica(message):
    dict_def.update({"Type1": "Механическая"})
    markup2 = types.InlineKeyboardMarkup()
    markup2.add(types.InlineKeyboardButton('Система охлаждения', callback_data='comm_def' + "Система охлаждения"))
    markup2.add(types.InlineKeyboardButton('Водяной насос', callback_data='comm_def' + 'Водяной насос'))
    markup2.add(types.InlineKeyboardButton('Шины', callback_data='comm_def' + 'Шины'))
    markup2.add(types.InlineKeyboardButton('Привод ГРМ', callback_data='comm_def' + 'Привод ГРМ'))
    markup2.add(types.InlineKeyboardButton('Другое', callback_data='comm_def' + 'Другое'))
    bot.send_message(message.chat.id, 'Выберите тип поломки', reply_markup=markup2, parse_mode='html')


def electric(message):
    dict_def.update({"Type2": "Электрическая"})
    markup3 = types.InlineKeyboardMarkup()
    markup3.add(types.InlineKeyboardButton('Антиблокировочная система (ABS)', callback_data='comm_def' + 'Антиблокировочная система (ABS)'))
    markup3.add(types.InlineKeyboardButton('Системы комфорта', callback_data='comm_def' + 'Системы комфорта'))
    markup3.add(types.InlineKeyboardButton('Электронная система торможения (EBS)', callback_data='comm_def' + 'Электронная система торможения (EBS)'))
    markup3.add(types.InlineKeyboardButton('Адаптивный круиз контроль (ACC)', callback_data='comm_def' + 'Адаптивный круиз контроль (ACC)'))
    markup3.add(types.InlineKeyboardButton('Другое', callback_data='comm_def' + 'Другое'))
    bot.send_message(message.chat.id, 'Выберите тип поломки', reply_markup=markup3, parse_mode='html')


def func_type2(message, call_funk):
    dict_def.update({"Type2": call_funk})
    chat_id = message.chat.id
    bot.send_message(chat_id, "При необходимости введите комментарий к поломке")
    bot.register_next_step_handler(message, func_describe)


def func_describe(message):
    chat_id = message.chat.id
    dict_def.update({"describe": message.text})
    add_row_json(dict_def) # записываем словарь в файл со всеми дефектами
    bot.send_message(chat_id, "Поломка успешно добавлена")


@bot.message_handler(func=lambda message: message)
def deleter(message):
    chat_id = message.chat.id
    deleter_message(chat_id, message, 10)


bot.infinity_polling()
