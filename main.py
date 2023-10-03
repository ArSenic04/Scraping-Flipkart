import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("Scraping Flipkart")
st.write("Scaping According to Pages in flipkart")
give_input = st.text_input("Enter a search term:")
page = st.slider("Number of Pages", 1, 30, 1)
button = st.button("Scrape Data")

if button:
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
                

    st.write("Scraped Data:")
    df = pd.DataFrame(product_data)
    st.write(df)

    # Download link
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        key='download-csv'
    )
