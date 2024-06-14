
from telebot import types
from function_and_data import *  # Да, я знаю что так неправильно, прости



@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id

    deleter(message)
    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Войти в систему', callback_data='sign_in'))
    send_message(chat_id, '🔐 <b>Войти</b> в систему для <u>старта</u>.', reply_markup=markup, parse_mode='html')


@bot.message_handler(commands=['main_menu'])
def main_message(message):
    chat_id = message.chat.id

    deleter(message)
    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if not is_sign_in(chat_id):
        start_message(message)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Зарегистрировать авто', callback_data='car_reg'))
        send_message(chat_id, 'main menu message.', reply_markup=markup)


@bot.message_handler(commands=['sign_out'])
def out_message(message):
    chat_id = message.chat.id

    # deleter(message)
    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if is_sign_in(chat_id):
        del_user_log(chat_id)
        send_message(chat_id, "🚪 <b>Сессия завершена.</b>\n", parse_mode='html')


# Добавил команду для очистки чата
@bot.message_handler(commands=['clear'])
def clear_all_message(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    del_message(chat_id)  # Удаление всех сообщений в чате


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    chat_id = callback.message.chat.id
    call_funk = callback.data
    message = callback.message

    deleter(message)

    add_message(message) # Добавление сообщения, которое ввёл пользователь

    match call_funk:
        case 'sign_in':
            sign_in(message)
        case 'car_reg':
            car_registration(message)
        case 'exit_reg':
            exit_registration(message)
        case 'add_device':
            add_device(message)
        case 'add_name':
            add_name(message)
        case 'add_gosnum':
            add_gosnum(message)
        case 'add_brand':
            add_brand(message)
        case 'add_wheels':
            add_wheels(message)
        case 'add_brandWs':
            add_brandWs(message)
        case 'end_reg':
            end_registration(message)


def get_passwd(message, login):
    chat_id = message.chat.id

    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    passwd = message.text
    if is_acreditation(login, passwd):
        send_message(chat_id, "✅ <b>Вход</b> в систему <u>выполнен.</u>\n", parse_mode='html')
        add_user_log(chat_id, login)
        main_message(message)
    elif passwd == '/start':  # for break from menu, do you think that we should add InlineKeyboardButton?
        start_message(message)
    elif passwd == '/sign_out':
        out_message(message)
    else:
        send_message(chat_id, "🚫 <b>Неверный</b> <u>пароль.</u> \nПовторите попытку.\n", parse_mode='html')
        bot.register_next_step_handler(message, get_passwd, login=login)


# Функция для регистрации пользователя
def get_login(message):
    chat_id = message.chat.id
    login = message.text

    deleter(message)
    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if is_registered(login):
        send_message(chat_id, "🔑 <b>Логин</b> есть <u>в системе.</u> \nВведите пароль.\n", parse_mode='html')
        bot.register_next_step_handler(message, get_passwd, login=login)
    elif login == '/start':  # for break from menu, do you think that we should add InlineKeyboardButton?
        start_message(message)
    else:
        send_message(chat_id, "🚫 <b>Логин</b> <u>не зарегистрирован</u> в системе. \nПовторите попытку.\n",
                     parse_mode='html')
        bot.register_next_step_handler(message, get_login)


def sign_in(message):
    chat_id = message.chat.id

    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if not is_sign_in(chat_id):
        send_message(chat_id, "💼 <b>Введите</b> логин компании.", parse_mode='html')
        bot.register_next_step_handler(message, get_login)
    else:
        main_message(message)


def car_registration(message, **kwags):
    chat_id = message.chat.id

    add_car_reg_log(chat_id, **kwags)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🚫', callback_data='exit_reg'))
    send_message(chat_id, '❗   ❗   Отменить регистрацию.  ❗  ❗', reply_markup=markup)
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('⚙️ Устройство', callback_data='add_device')
    btn2 = types.InlineKeyboardButton('🏢 Компания', callback_data='add_name')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('🚘 Гос. номер', callback_data='add_gosnum')
    btn4 = types.InlineKeyboardButton('🚗 Марка автомобиля', callback_data='add_brand')
    markup.row(btn3, btn4)
    btn5 = types.InlineKeyboardButton('🛞 Количество колес', callback_data='add_wheels')
    btn6 = types.InlineKeyboardButton('🔄 Марка шин', callback_data='add_brandWs')
    markup.row(btn5, btn6)
    markup.add(types.InlineKeyboardButton('Завершить регистрацию ✅', callback_data='end_reg'))

    send_message(chat_id, form_text(chat_id, kwags), parse_mode='html', reply_markup=markup)


def exit_registration(message):
    chat_id = message.chat.id
    del_car_reg_log(chat_id)
    deleter_message(chat_id, message, -10)
    send_message(chat_id, 'Регистрация завершена 🚫.')
    main_message(message)

def end_registration(message):
    chat_id = message.chat.id

    chat_id = str(chat_id)

    if chat_id in get_car_reg_log(chat_id):
        if 'gosnum' in get_car_reg_log(chat_id)[str(chat_id)].keys():
            save_car_reg_log(chat_id)
            send_message(chat_id, 'Регистрация завершена успешно ✅.')
            main_message(message)
        else:
            send_message(chat_id, 'Регистрация не завершина 🚫.\n Государственный номер - обязательный пункт регистрации.')
            car_registration(message)
    else:
        send_message(chat_id, 'Регистрация не завершина 🚫.\n Заполните форму!')
        car_registration(message)
    


#add_func
def add_device(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🆔 <b>Укажите</b> <u>ID</u> устройства', parse_mode='html')
    bot.register_next_step_handler(message, device_property)

def add_name(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🏢 <b>Введите</b> <u>наименование компании</u>', parse_mode='html')
    bot.register_next_step_handler(message, name_property)

def add_gosnum(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🚗 <b>Введите</b> государственный <u>номер автомобиля</u>', parse_mode='html')
    bot.register_next_step_handler(message, gosnum_property)

def add_brand(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🚘 <b>Укажите</b> <u>марку автомобиля</u>', parse_mode='html')
    bot.register_next_step_handler(message, brand_property)

def add_wheels(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🛞 <b>Введите</b> количество <u>колёс</u> автомобиля', parse_mode='html')
    bot.register_next_step_handler(message, wheels_property)

def add_brandWs(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🔄 <b>Укажите</b> <u>марку шин</u>', parse_mode='html')
    bot.register_next_step_handler(message, brandWs_property)


#property
def device_property(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    text = message.text
    send_message(chat_id, f'Девайс {text} добавлен')
    car_registration(message, device=text)

def name_property(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    text = message.text
    send_message(chat_id, f'Крания {text} добавлена')
    car_registration(message, name=text)

def gosnum_property(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    text = message.text
    send_message(chat_id, f'Государственный номер {text} добавлен')
    car_registration(message, gosnum=text)


def brand_property(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    text = message.text
    send_message(chat_id, f'Марка колес {text} добавлена')
    car_registration(message, brand=text)


def wheels_property(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    text = message.text
    send_message(chat_id, f'Кол-во колес {text} добавлено')
    car_registration(message, wheels=text)


def brandWs_property(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    text = message.text
    send_message(chat_id, f'Брент колес {text} добавлен')
    car_registration(message, brandWs=text)


@bot.message_handler(func=lambda message: message)
def deleter(message):
    chat_id = message.chat.id
    deleter_message(chat_id, message, 10)


bot.infinity_polling()
