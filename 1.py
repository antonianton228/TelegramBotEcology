import telebot
import json
import requests
import json

bot = telebot.TeleBot('5318941676:AAE65AOZ11ylYJJmajr1PoJ2yM41xMpTVLo')

flag = True


@bot.message_handler(content_types=['text'])
def start(message):
        global flag
        if message.text == '/start':
                bot.send_message(message.from_user.id, '''Здравствуйте! 
Я бот, который поможет вам сохранить Землю в чистоте. 🌱♻️
Я подскажу вам, где находится ближайший пункт по сортировке отходов. Напишите /find для нахождения ближайших сортировок. А так же заходите на наш сайт: https://blooming-headland-96587.herokuapp.com/''')
        elif message.text == '/find':
                bot.send_message(message.from_user.id, "Отправьте мне вашу геолокацию")
        elif message.text == '/report':
                bot.send_message(message.from_user.id, "Отправьте мне геолокацию сортировки.")
                flag = False
        elif message.text == 'aaaddd':
                with open('reports.json', 'r', encoding='utf-8') as fh:
                        bot.send_document(message.from_user.id, fh)


@bot.message_handler(content_types=['location'])
def find(message):
        global flag, dict_of_reports
        if flag:
                print(message.location.longitude, message.location.latitude)
                bot.send_message(message.from_user.id, 'Начинаю поиск')
                lon, lat = message.location.longitude, message.location.latitude

                dict_of_cit = requests.get('https://xn--1-otblt.xn--p1ai/map/rm.php?city=-1').json()
                cur_cit = {'id': '1', 'lat': '55.7580321449', 'lng': '37.6168444863', 'title': 'Москва'}
                cur_c = 1000000000
                for i in dict_of_cit:
                        if (abs(lat - float(i['lat'])) ** 2 + abs(lon - float(i['lng'])) ** 2) ** 0.5 < cur_c:
                                cur_cit = i
                                cur_c = (abs(lat - float(i['lat'])) ** 2 + abs(lon - float(i['lng'])) ** 2) ** 0.5
                id = cur_cit['id']

                dict_of_rec = requests.get(f'https://сми1.рф/map/rm.php?city={id}').json()
                result = []
                metr = 0.0001
                while len(result) <= 5:
                        result = []
                        metr += 0.0001
                        for i in dict_of_rec:
                                lat1, lon1 = float(dict_of_rec[i]['lat']), float(dict_of_rec[i]['lng'])
                                if abs(lon - lon1) <= metr and abs(lat - lat1) <= metr:
                                        result.append(dict_of_rec[i])
                print(result)

                for i in result:
                        bot.send_message(message.from_user.id, i['title'])
                        bot.send_location(message.from_user.id, *tuple((float(i['lat']), float(i['lng']))))
                bot.send_message(message.from_user.id,
                                 'Поиск окончен. Если бот не нашел сортировки, о которых вам известно, то напишите команду /report и отправьте обратную связь.')
        else:
                with open('reports.json', 'r', encoding='utf-8') as fh:
                        dict_of_reports = json.load(fh)
                dict_of_reports[str(len(dict_of_reports))] = str(message)
                with open('reports.json', 'w', encoding='utf-8') as fh:
                        fh.write(json.dumps(dict_of_reports, ensure_ascii=False))
                flag = True
                bot.send_message(message.from_user.id,
                                 'Спасибо за обратную связь')


bot.polling(none_stop=True)
