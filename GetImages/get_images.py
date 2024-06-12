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

s = webdriver.ChromeService(executable_path='C:\\Users\\Usern\\Projects\\Python\\PlanetClassifier\\GetImages\\chromedriver.exe')
driver = webdriver.Chrome(service=s)

search_URL = "https://www.google.com/search?q=earth&tbm=isch&ved=2ahUKEwiIqOPA8NSGAxU9JGIAHVkOC5kQ2-cCegQIABAA&oq=earth&gs_lp=EgNpbWciBWVhcnRoMg0QABiABBixAxhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMg0QABiABBixAxhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMg0QABiABBixAxhDGIoFMgoQABiABBhDGIoFSNMKUJ0JWJ0JcAB4AJABAJgBTKABlwGqAQEyuAEDyAEA-AEBigILZ3dzLXdpei1pbWfCAgUQABiABIgGAQ&sclient=img&ei=PfVoZsiVO73IiLMP2ZysyAk&bih=739&biw=1536&cs=1&hl=en-US"
driver.get(search_URL)

open = True

start = input("Waiting for user input...")

# scroll up
driver.execute_script("window.scrollTo(0,0);")

page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class':"eA0Zlc WghbWd FnEtTd mkpRId m3LIae RLdvSe qyKxnc ivg-i PZPZlf GMCzAd"})

len_containers = len(containers)
print(f"Found {len_containers} images")

folder_name = 'ImageData\Earth'
for i in range(1, len_containers+1):
    if i%25 == 0:
        continue

    xpath = f"""//*[@id="rso"]/div/div/div[1]/div/div/div[{i}]"""

    driver.find_element(By.XPATH, xpath).click()
    time.sleep(1.5) #delaying so that full res image can load

    img_element = driver.find_element(By.XPATH, """//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]""")
    img_URL = img_element.get_attribute("src")

    download(img_URL, folder_name, i)
    