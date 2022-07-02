import telebot
from dadata import Dadata
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PIL import Image, ImageEnhance
from telebot import types
import os
from selenium.webdriver.chrome.options import Options

bot = telebot.TeleBot('5318941676:AAE65AOZ11ylYJJmajr1PoJ2yM41xMpTVLo')
dadata_token = "6c6c51197b8eb6501d4d469c891aab2613f67420"

dadata = Dadata(dadata_token)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id,
                         "Здравствуйте, я бот, который поможет вам сохранить землю в чистоте. Я подскажу вам, где находится бллижайший пункт по сортировке отходов, а так же смогу помочь с определением типа отходов. Напишите /find для нахождения ближайших сортировок, напишите /opr для помощи с определением.")
    elif message.text == '/find':
        bot.send_message(message.from_user.id, "Отправьте мне вашу геолокацию")

    elif message.text == '/opr':
        bot.send_message(message.from_user.id, "Отправьте мне вашу геолокацию")
    elif message.text == 'Узнать значение цветов':
        bot.send_message(message.from_user.id, "Отправьте мне вашу геолокацию")
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
    # result = 'Россия, Москва, Москва, округ Текстильщики, 109518, Саратовская Улица'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    bot.send_message(message.from_user.id, "Ищу адреса")

    driver.get('https://recyclemap.ru/#')
    time.sleep(3)
    if typee != 0:
        driver.find_element(By.CSS_SELECTOR, f'a[data-id="{typee - 2}"]').click()
    element = driver.find_element(By.CLASS_NAME, "mapboxgl-ctrl-geocoder--input")
    element.send_keys(result)
    time.sleep(0.5)
    element.send_keys(Keys.ENTER)
    time.sleep(1.5)
    element = driver.find_element(By.ID, 'alert')
    driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)
    element = driver.find_element(By.TAG_NAME, 'html')
    t = driver.find_element(By.CLASS_NAME, 'locat_near')
    text = t.text
    adres = text.split('\n')[1::2]
    names = text.split('\n')[::2]
    coords = []
    for i in adres:
        driver.get('https://yandex.ru/maps/')
        element = driver.find_element(By.CLASS_NAME, "input__control._bold")
        element.send_keys(i)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        element = driver.find_element(By.CLASS_NAME, "toponym-card-title-view__coords-badge")
        coords.append(element.text)
    driver.close()
    print(coords)
    for i, j in zip(coords, names):
        bot.send_message(message.from_user.id, j)
        bot.send_location(message.from_user.id, *tuple(map(float, i.split(', '))))

    # im = Image.open('1.png')
    # enhancer = ImageEnhance.Brightness(im)
    # im = enhancer.enhance(2)
    # im.crop((400, 100, 1920, 800)).save('1.png')
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # btn1 = types.KeyboardButton("Узнать значение цветов")
    # markup.add(btn1)
    # img = open("1.png", 'rb')
    # bot.send_photo(message.chat.id, img, reply_markup=markup)


bot.polling(none_stop=True)

