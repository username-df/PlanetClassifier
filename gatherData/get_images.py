import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

def download(url, fn, num):
    response = requests.get(url)

    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

    if response.status_code == 200:
        with open(os.path.join(fn, str(num)+".jpg"), 'wb') as file:
            file.write(response.content)

s = webdriver.ChromeService(executable_path='C:\\Users\\Usern\\Projects\\Python\\PlanetClassifier\\gatherData\\chromedriver.exe')
driver = webdriver.Chrome(service=s)

search_URL = "https://www.google.com/search?q=earth&sca_esv=68041e448ebf4032&sca_upv=1&hl=en&udm=2&cs=1&biw=1036&bih=659&ei=aC2DZojFMdeZptQPgPaJ2AE&ved=0ahUKEwiImZLd8YaHAxXXjIkEHQB7AhsQ4dUDCBE&uact=5&oq=earth&gs_lp=Egxnd3Mtd2l6LXNlcnAiBWVhcnRoMg0QABiABBixAxhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMg0QABiABBixAxhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFSOELUJ0FWKAJcAJ4AJABAJgBRaABoQKqAQE1uAEDyAEA-AEBmAIHoALEAsICCBAAGIAEGLEDwgIFEAAYgATCAgQQABgDmAMAiAYBkgcBN6AHxhg&sclient=gws-wiz-serp"
driver.get(search_URL)

start = input("Waiting for user input...")

# scroll up
driver.execute_script("window.scrollTo(0,0);")

page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class':"eA0Zlc WghbWd FnEtTd mkpRId m3LIae RLdvSe qyKxnc ivg-i PZPZlf GMCzAd"})

len_containers = len(containers)
print(f"Found {len_containers} images")

folder_name = 'ImageData\\Earth'
for i in range(1, len_containers+1):
    xpath = f"""//*[@id="rso"]/div/div/div[1]/div/div/div[{i}]"""

    try:
        element = driver.find_element(By.XPATH, xpath)

        if element.get_attribute("class") == "BA0zte":
            continue

        element.click()
        time.sleep(1.5) #delaying so that full res image can load
       
        img_element = driver.find_element(By.XPATH, """//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img[1]""")

        img_URL = img_element.get_attribute("src")
        download(img_URL, folder_name, i+518)

    except:
        continue

    print(i)