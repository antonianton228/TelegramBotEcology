from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()


driver.get('https://recyclemap.ru/')
time.sleep(2)
element = driver.find_element(By.CLASS_NAME, "mapboxgl-ctrl-geocoder--input")
element.send_keys('Россия Москва Москва 109518 Саратовская улица 19')
element.send_keys("", Keys.ENTER)
time.sleep(2)
# login = driver.find_element_by_id('search_left').send_keys('Россия Москва Москва 109518 Саратовская улица 19')
driver.get_screenshot_as_file("LambdaTestVisibleScreen.png")
driver.close()