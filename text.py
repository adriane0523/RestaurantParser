import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from random import randint

from webdriver_manager.chrome import ChromeDriverManager
import requests
import random
import json
import time
import pyautogui

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()


import requests
apikey = "ee0d02cd9400c5a1544bf1afc936316e3025440d"
response = requests.get("https://proxy.webshare.io/api/proxy/list/", headers={"Authorization": "Token " + apikey})
json_response = response.json()

first = json_response["results"][0]
first_ip = first["proxy_address"]
first_port = first["ports"]["http"]

proxy_ip = (str)(first_ip) + ":" + (str)(first_port)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % proxy_ip)
driver_ = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


random_time = random.randint(1, 5)
print("wait: ", random_time, "secs...")
time.sleep(random_time)
driver_.get(u)

time.sleep(1)
pyautogui.typewrite(first["username"] )
pyautogui.press('tab')
pyautogui.typewrite(first["password"])
pyautogui.press('enter')




sql = ''' INSERT INTO database_restaurant(id,name,direction,rest_hours,phone,price, payment, categories, other, stars, count, links, ypLink)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) '''
value1 = (1, "test", "test", "test", "test", "test", "test", "test", "test", "test", 'test', "test", "test")


c.execute(sql, value1)
print(c.lastrowid)

for row in c.execute('SELECT * FROM database_restaurant ORDER BY id'):
        print(row)
        print("\n")
conn.commit()
c.close()