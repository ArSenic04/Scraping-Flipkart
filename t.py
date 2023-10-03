import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# options=webdriver.ChromeOptions()
# options.add_experimental_option("detach",True)

# driver = webdriver.Chrome(options=options)
give_input = input("Enter: \n")
page = 2
product_data = []
for p in range(1, page + 1):
    url = 'https://www.flipkart.com/search?q={give_input}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page={p}'.format(
        give_input=give_input, p=p)
    code = requests.get(url)
    soup = BeautifulSoup(code.text, 'html.parser')
    names = soup.find_all("div", {"class": "_4rR01T"})
    if names:
        prices = soup.find_all("div", {"class": "_30jeq3 _1_WHN1"})
        ratings = soup.find_all("div", {"class": "_3LWZlK"})
        for name, price, rating in zip(names, prices, ratings):
            product_data.append(
                {'Name': name.text, 'Price': price.text, 'Rating': rating.text})
    else:
        names = soup.find_all("a", {"class": "s1Q9rs"})
        ratings = soup.find_all("div", {"class": "_3LWZlK"})
        prices = soup.find_all("div", {"class": "_30jeq3"})

        for name, price, rating in zip(names, prices, ratings):
            product_data.append(
                {'Name': name.text, 'Price': price.text, 'Rating': rating.text})

df = pd.DataFrame(product_data)
print(df)
