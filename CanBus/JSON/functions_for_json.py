import json


def read_inf(file_name):
    with open(file_name, 'r', encoding="utf-8") as file:
        return json.load(file)


cars = read_inf("data/Cars.json")
companies = read_inf("data/Companies.json")
drivers = read_inf("data/Drivers.json")
sensors = read_inf("data/Sensors.json")
users = read_inf("data/Users.json")
defects = read_inf("data/Defects.json")
wheels = read_inf("data/Wheels.json")

# тут просто куча функций, часть используется, остальные могут понадобится


# получить id компании по ее названию
def get_id_company(company_name):
    return [i.get('ID_company') for i in companies if i.get("Name") == company_name]


# получить id юзера по номеру телефона
def get_id_user_login(login):
    return [i.get('ID_user') for i in users if i.get('Login') == login][0]


# Получить всех пользователей одной компании определенного типа (Водитель/Владелец - type_)
def type_company(id_company, type_):
    drivers_id = [i.get("ID_user") for i in users if
                  i.get("Type") == type_ and int(i.get("Company")) in id_company]
    return drivers_id


# здесь проверка зарегался ли пользователь с проверкой принадлежности опред.классу и без
def registered_users_login(type_):
    if type_ == "":
        log_users = [i.get("Login") for i in users]
    else:
        log_users = [i.get("Login") for i in users if i.get("Type") == type_]
    return log_users


# проверка правильности пароль
def registered_users_password(type_):
    if type_ == "":
        pas_users = [i.get("Password") for i in users]
    else:
        pas_users = [i.get("Password") for i in users if i.get("Type") == type_]
    return pas_users


# Получение сводки всей инфы по юзерам определенного типа (type_) одной компании (company_id)
def get_inf_users(company_id, type_):
    return ([(i.get("ID_user"), i.get("Full name"), i.get("Birthday")) for i in users
             if i.get('Type') == type_ and i.get("Company") == company_id])


# Получить все машины опред.признака (type_ может быть Company, Driver), inf - знач., которое должен этот признак принимать
def get_car(inf, type_):
    return [i.get("Registration_number") for i in cars if i.get(type_) == inf]



# Получить все инфу об определенных машинах (с опред. id)
def get_inf_car(id_car):
    return [(i.get('Registration_number'), i.get('Driver'), i.get('Brand')) for i in cars if i.get('Registration_number') in id_car]


# Получить все колеса машины
def all_wheel_car():
    print("Регистрационный номер машины")
    reg_car = int(input())
    car_id = [i.get("ID_wheel") for i in wheels if i.get("Car_number") == reg_car]
    return car_id


# Получить сенсоры колес опред.машины
def car_wheels_sensors(reg_car):
    sensors_id = [int(i.get("Sensors")) for i in wheels if i.get("Car_number") == reg_car]
    sensors_inf = [(i.get("ID_sensors"), i.get("Type"), i.get("Readings"))
                   for i in sensors if i.get("ID_sensors") in sensors_id]
    return sensors_inf


# Получить сводку всех сенсоров машины
def all_sensors_car(reg_car):
    car_sensors = [int(i.get("Sensors")) for i in cars if i.get("Registration_number") == reg_car]
    car_sensors_inf = [(i.get("ID_sensors"), i.get("Type"), i.get("Readings"))
                       for i in sensors if i.get("ID_sensors") in car_sensors]
    return car_sensors_inf, car_wheels_sensors(reg_car)


# Получить тип и описание дефектов машины по опред. признаку (type_) type_ может быть = car_id, driver_id
def get_defects_driver_car(value, type_):
    return [(i.get("Type1"), i.get("Type2"), i.get("describe")) for i in defects if str(i.get(type_)) == str(value)]


# Получить id пользователя по номеру телефона
def get_id_driver_phone(login):
    return [i.get("ID_user") for i in users if str(i.get("Login")) == str(login)]


def deleter_message(chat_id, message, count_del=1):
    message_id = message.id
    if count_del < 0:
        del_list = range(0, count_del, -1)
    else:
        del_list = range(count_del)

    for i in del_list:
        try:
            bot.delete_message(chat_id, message_id - i)
        except Exception as error:
            continue


# получить id последнего добавленного дефекта
def get_id_df():
    b = json.load(open('data/Defects.json', encoding='utf-8'))
    return b[len(b) - 1]['ID_defect'] + 1


# добавить дефект
def add_row_json(dict_):
    b = json.load(open('data/Defects.json', encoding='utf-8'))
    b.append(dict_)
    json.dump(b, open('data/Defects.json', 'w'))


# Получить опред.признак пользователя
def get_by_id(id_, inf):
    return [i.get(inf) for i in users if i.get("ID_user") == id_][0]
