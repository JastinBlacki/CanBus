import telebot
from main import get_state, get_graph
from functions_for_json import registered_users_login
import json

token = '6971909537:AAGbRyjyE2WfLqLpBxZobDuLCo8iSjM21BY'
bot = telebot.TeleBot(token)


# Функция для проверки, зарегистрирован ли пользователь
def is_registered(phone_number):
    registered = registered_users_login("")
    return str(phone_number) in registered


# Функция для регистрации пользователя
def register_user(message):
    chat_id = message.chat.id
    phone_number = message.text

    if not is_registered(phone_number):
        with open('registered_users.json', 'r') as file:
            registered_users = json.load(file)

        registered_users[phone_number] = str(chat_id)

        with open('registered_users.json', 'w') as file:
            json.dump(registered_users, file)

        bot.send_message(chat_id,
                         f"Вы успешно зарегистрированы с номером телефона: {phone_number}, можете написать команду /help для того чтобы узнать функционал бота")
    else:
        bot.send_message(chat_id,
                         "Вы уже зарегистрированы, напишите команду /help для того чтобы узнать функционал бота")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Здравствуй, здесь ты получищь статистику с твоего mvp, напиши свой номер телефона в виде - '+79999999999' для регистрации (тут могла быть информация по давлению в твоих шинах)")
    bot.register_next_step_handler(message, register_user)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id,
                     "1 /start - начало работы\n2 /help - узнать функции бота\n3 возможно запросить интересующие вас текущие данные с датчика (сейчас только давление и температура)\n"
                     "4 данные за всё время в виде графика\n\nВ БУДУЩЕМ:\n1 получить данные за определённый промежуток времени в виде удобного графика\n2 получить данные в виде любого файла\n"
                     "3 получить информацию в виде голосового сообщения\n4 переслать сообщение водителю-косячнику\n5 получить метку на карте текущего положения машин\n!!ПОЯВИТСЯ GPT ПОМОЩНИК")


@bot.message_handler(content_types="text")
def message_reply(message):
    if "температ" in message.text.lower():
        data = get_state()
        bot.send_message(message.chat.id, f'Текущее состояние датчика температуры = {data[0]}')
    elif "давлен" in message.text.lower():
        data = get_state()
        bot.send_message(message.chat.id, f'Текущее состояние датчика давления = {data[1]}')
    elif "график" in message.text.lower():
        get_graph(message.chat.id)
        bot.send_photo(message.chat.id, open(f"graph_{message.chat.id}", 'rb'))
    else:
        bot.send_message(message.chat.id,
                         'К сожалению у меня пока нет GPT, поэтому я вас не понял. Повторите ещё раз свой запрос')


bot.infinity_polling()