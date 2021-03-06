import telebot
from dadata import Dadata
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PIL import Image
from telebot import types
from selenium.webdriver.chrome.options import Options

bot = telebot.TeleBot('5318941676:AAE65AOZ11ylYJJmajr1PoJ2yM41xMpTVLo')
dadata_token = "6c6c51197b8eb6501d4d469c891aab2613f67420"

dadata = Dadata(dadata_token)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Здравствуйте, я бот, который поможет вам сохранить землю в чистоте. Я подскажу вам, где находится бллижайший пункт по сортировке отходов, а так же смогу помочь с определением типа отходов. Напишите /find для нахождения ближайших сортировок, напишите /opr для помощи с определением.")
    elif message.text == '/find':
        bot.send_message(message.from_user.id, "Отправьте мне вашу геолокацию")
    elif message.text == '/opr':
        bot.send_message(message.from_user.id, "Отправьте мне вашу геолокацию")
    elif message.text == 'Узнать значение цветов':
        img = open('inf.png', 'rb')
        bot.send_photo(message.from_user.id, img)
    else:
        bot.send_message(message.from_user.id, "Напишите /start")


@bot.message_handler(content_types=['location'])
def find(message):
    lon, lat = message.location.longitude, message.location.latitude
    print(message.location)
    result = dadata.geolocate(name="address", lat=lat, lon=lon)[0]
    country = result['data']['country']
    region = result['data']['region']
    city = result['data']['city']
    postal_code = result['data']['postal_code']
    street = result['data']['street']
    street_type_full = result['data']['street_type_full']
    house = result['data']['house']
    result = ' '.join([country, region, city, postal_code, street, street_type_full, house])
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()

    driver.get('https://recyclemap.ru/')
    element = driver.find_element(By.CLASS_NAME, "mapboxgl-ctrl-geocoder--input")
    element.send_keys(result)
    time.sleep(1)
    element.send_keys(Keys.ENTER)
    time.sleep(1)
    driver.get_screenshot_as_file("MapScreen.png")
    driver.close()
    im = Image.open('MapScreen.png')
    im.crop((400, 100, 1920, 800)).save('MapScreen.png')
    img = open('MapScreen.png', 'rb')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Узнать значение цветов")
    markup.add(btn1)
    bot.send_photo(message.chat.id, img, reply_markup=markup)


bot.polling(none_stop=True)


