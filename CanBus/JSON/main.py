import requests
import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64

url = 'https://dev.rightech.io/api/v1/objects'
headers = {
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2NTk2Nzg4Mzk2YmE1ZjY2ZTBhNjZlNTkiLCJzdWIiOiI2NTk1YTE1ZjczNWY1ZDcxZTIwMWNhZmYiLCJncnAiOiI2NTk1YTE1ZjczNWY1ZDcxZTIwMWNhZmUiLCJvcmciOiI2NTk1YTE1ZjczNWY1ZDcxZTIwMWNhZmUiLCJsaWMiOiI1ZDNiNWZmMDBhMGE3ZjMwYjY5NWFmZTMiLCJ1c2ciOiJhcGkiLCJmdWxsIjpmYWxzZSwicmlnaHRzIjoxLjUsImlhdCI6MTcwNDM2MDA2NywiZXhwIjoxNzA2OTAwNDAwfQ.RHNCW9zKCD_YoY6YKZd5QRywq4yZs8vJtkT2RspjHkM',
    'Content-Type': 'application/json'
}


def my_utc_from_timestamp(ts):
    return datetime.datetime.utcfromtimestamp(ts // 1000)


def timestamp_from_utc(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp()


def get_state():
    try:
        response = requests.get(url, headers=headers)
        # Проверяем успешность запроса
        if response.status_code == 200:
            data = response.json()  # Если ответ в формате JSON
            # print(data)
            # print(data[0]["state"]["temperature"])
            return (data[0]["state"]["temperature"], data[0]["state"]["humidity"])
        else:
            print(f'Ошибка запроса: {response.status_code}')
            print(response.text)

    except Exception as e:
        print(f'Произошла ошибка: {e}')


def get_time_line_data():
    global url

    data = 0
    pressure = {}
    temperature = {}

    try:
        response = requests.get(url, headers=headers)

        # Проверяем успешность запроса
        if response.status_code == 200:
            data = response.json()  # Если ответ в формате JSON
        else:
            print(f'Ошибка запроса: {response.status_code}')
            print(response.text)

    except Exception as e:
        print(f'Произошла ошибка: {e}')

    url = f'https://dev.rightech.io/api/v1/objects/{data[0]["_id"]}/packets?withChildGroups=true&ofType=telemetry&snaps=true&nolimit=true&streamed=true&from=1704339181541&to=1704425581541&db=pgts'

    try:
        response = requests.get(url, headers=headers)

        # Проверяем успешность запроса
        if response.status_code == 200:
            data = response.json()  # Если ответ в формате JSON
        else:
            print(f'Ошибка запроса: {response.status_code}')
            print(response.text)

    except Exception as e:
        print(f'Произошла ошибка: {e}')

    # print(my_utc_from_timestamp(data[0]["time"]))
    # print(data)
    for i in data:
        if 'humidity' in i:
            pressure[str(my_utc_from_timestamp(i["time"]))] = i['humidity']
        elif 'temperature' in i:
            temperature[str(my_utc_from_timestamp(i["time"]))] = i['temperature']

    temperature = dict(sorted(temperature.items()))
    pressure = dict(sorted(pressure.items()))

    return temperature, pressure


def get_graph(chat_id):
    data = get_time_line_data()

    dates_temp = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in data[0].keys()]
    dates_press = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in data[1].keys()]

    numbers_temp = [int(number) for number in data[0].values()]
    numbers_press = [int(number) for number in data[1].values()]

    # Задаем размер графика
    plt.figure(figsize=(15, 6))

    # Построение графиков
    plt.plot(dates_temp, numbers_temp, label='Температура', color="green")
    plt.plot(dates_press, numbers_press, label='Давление', color="blue")

    # Добавление легенды
    plt.legend()

    plt.xlabel('Дата и время')
    plt.ylabel('Значение')
    plt.title('Давление и Температура')

    # plt.show()

    # Возвращаем график в виде изображения
    img_buf = BytesIO()
    plt.savefig(f"graph_{chat_id}", format='png')
    img_buf.seek(0)


    # Очищаем текущий график
    plt.clf()