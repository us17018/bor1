import requests
import time
from pprint import pprint

API_URL: str = 'https://api.telegram.org/bot'  # ссылка на бота
BOT_TOKEN: str = '6245798122:AAG9WztsZo4Flm9pKdT2NYQk8MZQQLDCWMw'  # ключик
TEXT: str = 'ку'  # текст который отправится при любом сообщении
MAX_COUNTER: int = 100  # количество восроизводства цикла

offset: int = -2  # самый новый апдейт
counter: int = 0  # счетчик для взаимодействия с MAX_COUNTER чтобы программа не была вечно(пока что)
chat_id: int


while counter < MAX_COUNTER:  # если MAX_COUNTER == 0 то бот больше не отвечает

    print('attempt =', counter)  # Чтобы видеть в консоли, что код живет
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()  # перенос API в JSON
    updates2 = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset}').json()
    updates3 = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset - 1}').json()


    if updates['result']:
        pprint(updates['result'][0]['update_id'])
        pprint(updates2['result'][0]['update_id'])
        pprint(updates3['result'][0]['update_id'])

        for result in updates['result']:
            offset = result['update_id']  # получаем номер апдейта(начиная с 1)
            chat_id = result['message']['from']['id']  # номер чата из которого пришел апдейт
            requests.get(
                f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')  # отправка нужного сообщений я в

    time.sleep(1) # небольшая остоновка для лучшей работы сервера
    counter += 1