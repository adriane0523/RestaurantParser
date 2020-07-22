from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from random import randint

from webdriver_manager.chrome import ChromeDriverManager
import requests
import random
import json
import pyautogui

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 


import sqlite3
#----------------------------------------------- 
def get_proxies():

    proxy_web_site = 'http://free-proxy.cz/en/proxylist/country/US/all/ping/all'
    response = requests.get(proxy_web_site)
    page_html = response.text
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.find_all("tr")

    proxies = set()

    for i in containers:
        print(i)
        ip = containers.find_all("td")[i].text
        port = containers.find_all("td")[i+1].text
        https = containers.find_all("td")[i+6].text
        print("\nip address : {}".format(ip))
        print("port : {}".format(port))
        print("https : {}".format(https))
    
        if https == 'yes':
            proxy = ip + ':' + port
            proxies.add(proxy)
                
    return proxies 


#----------------------------------------------- 
def check_proxies():
    working_proxies = []
    
    proxies = open_proxy_txt()          
    test_url = 'https://www.yellowpages.com/'    
    for i in proxies:
        print("\nTrying to connect with proxy: {}".format(i))
        try:
            response = requests.get(test_url, proxies={"http": i, "https": i}, timeout = 5)
            print(response.json())
            print("This proxy is added to the list. Have a lovely day!")
            working_proxies.append(i)
            
        except:
            print("Skipping. Connnection error")

    return working_proxies

#----------------------------------------------- 
def open_url_text():
    f = open("url.txt","r")
    url_list = []
    if f.mode == 'r':
        contents = f.read()
      
        url = ""
        for i in contents:
            
            if (i != "\n"):
                url += i
            else:
                
                url_list.append(url)
                url = ""
            
    return url_list
        
#----------------------------------------------- 
def open_proxy_txt():
    f = open("proxy.txt","r")
    url_list = []
    if f.mode == 'r':
        contents = f.read()
      
        url = ""
        for i in contents:
            
            if (i != "\n"):
                url += i
            else:
                
                url_list.append(url)
                url = ""
            
    return url_list
#-----------------------------------------------
def web_parser():
    id_num= 2340
 
    driver_ = webdriver.Chrome(ChromeDriverManager().install())
    categories_list = []
    url = open_url_text()

    #apikey = "ee0d02cd9400c5a1544bf1afc936316e3025440d"
    apikey = "6c598d0205ff02c2c019da91bf82070796b73895"
    response = requests.get("https://proxy.webshare.io/api/proxy/list/", headers={"Authorization": "Token " + apikey})
    json_response = response.json()
        

    for u in url:
        flag = True
        page_soup = None
        prox = None
        retry = 0
        proxy_ip = ""
        while(flag):
            try:

                # Load proxy option

                first = json_response["results"][random.randint(0, (json_response["count"] - 1 ) )]
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


                random_time = random.randint(15, 20)
                print("Loading: ", random_time, "secs...")
                time.sleep(random_time)

                myElem = WebDriverWait(driver_, 10)

                page_html = driver_.page_source
                page_soup = soup(page_html, "html.parser")

          
                flag = False
                
            except:
                if (retry  == 3):
                    flag = False
                    print("Failed after 3 attempts, skipping: " + u)
                else:
                    retry = retry + 1
                    print("Retrying...")

        container = page_soup.find(id = "business-info")
        
        #restaurant name
        restName = ""
        try:
            salesinfo = page_soup.find( class_="sales-info")
            restName = salesinfo.find_all('h1')[0].text

        except:
            restName = "No Name"
        
        stars = ""
        try:
            stars =(str)(page_soup.find( class_="ta-rating" ))
        
            temp = stars[38:]
   
            temp2 = temp[0 : len(temp) - 8]
            stars = temp2[0] + "." + temp2[2]



          
        except:
            stars = "0"
        
        
        review_count = 0
        try:
            review_count =(str)(page_soup.find( class_="ta-count").text)
            temp = review_count[1:]

            review_count = temp[0: len(temp) - 9]
            
          
          

        except:
            review_count = 0



        #Get direction of the restaurant
        direction = "No Direction"
        try:
            direction = page_soup.find('h2', class_="address").text
        except:
            direction = "No Direction"
        

        #get phone number of the restaurant
        phone = ""
        try:
            phone = page_soup.find('p',class_ = "phone").text
        except:
            phone = ""

        
        #this gets the payment method accepted from the restaurant
        payment = "No Payment"
        try:
            payment = container.find(class_ = "payment").text
            #print(payment)
        except:
            payment = "No Payment"


        restaurant_price = ""
        count = 0
        holder = container.text
        for c in holder:
            if ( holder[count] == "P" and holder[count+1] == "r" and holder[count+2] == "i" and holder[count+3] == "c" and holder[count+4] == "e" 
                and holder[count+5] ==" " and holder[count+6] == "R" and holder[count+7] == "a" and holder[count+8] == "n" and holder[count+9] == "g"
                and holder[count+10]== "e"):
    
                    for b in range (5):
                        if (holder[count + 10 + b] == "$"):
                            restaurant_price = restaurant_price + holder[count + 10 + b]
                            
            count = count + 1
        
        #this gets the link of the restaurant website
        link = "No Link"
        try:
       
            website = container.find(class_="other-links")
            link = website.get('href').text
        except:
            link = "No Link"
        

        restHours = ""
        try:
            #this get the hours of the restaurant
            restHours= container.find(class_= "open-details").text  
          
        except:
            restHours = ""

        
        #This gets the categories of the restaurant
        result_categories = ""
        try:
            categories = container.find('dd',class_="categories")
            for i in categories:
                result_categories = result_categories + i.text + "|"

               

           
            for i in result_categories:
                if i not in categories_list:
                    categories_list.append(i)

            
        except:
            result_categories = "No Categories"

       
        restOther = ""
        try:
            #Get other information of the restaurant
            other = container.find('dd', class_="other-information")
            for i in other.findAll('p'):  
                other =  i.text.replace("\u00a0", " ")
                other =  i.text.replace(",", "|")
                restOther = restOther + other + ","
          

        except:
            restOther = ""
        
        otherLinks = ""

        try:
            otherLinks = container.find('dd',class_ ="weblinks").text
     
            

        except:
            otherLinks = ""
        
        ypLink = u


        print("\n")
        print("name:",restName)
        print("direction:",direction)
        print("rest hours:", restHours)
        print("phone:", restHours)
        print("price:", restaurant_price)
        print("payment:", payment)
        print("categories:",result_categories)
        print("other:", restOther)
        print("----------------------")
        print("stars:", stars)
        print("count:", review_count)
        print("other links:", otherLinks)
        print("yellow pages link:", ypLink)

        driver_.close()
        driver_ = webdriver.Chrome(ChromeDriverManager().install())     
        



        sql = ''' INSERT INTO database_restaurant(id,name,direction,rest_hours,phone,price, payment, categories, other, stars, count, links, ypLink)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        value1 = (id_num, restName, direction, restHours, restHours, restaurant_price, payment, result_categories, restOther, stars, review_count, otherLinks, ypLink)
        id_num = id_num + 1
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute(sql, value1)
        conn.commit()
        c.close()
        

    
    print("Done Parsing")
    file1 = open("categories.txt","w")  
    for i in categories_list:
        file1.write(i + "\n")

    file1.close() #to change file access modes  
    print("Done writing to file")





if __name__ == "__main__":
 
    web_parser()
