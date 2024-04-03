import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import uuid
import random
import string
import pandas as pd
import base64

def generate_random_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("News Data")

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Make the driver headless
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.indiatvnews.com/topic/weather')

news_items = driver.find_elements(By.CSS_SELECTOR, "div.row.newsListBox")

news = []

for item in news_items:
    headline = item.find_elements(By.CSS_SELECTOR,"h3.title")
    newsdesc = item.find_elements(By.CSS_SELECTOR,"p.dic")
    daydatetime = item.find_elements(By.CSS_SELECTOR,"span.deskTime")
    image = item.find_elements(By.CSS_SELECTOR,"img")
    news_url = item.find_elements(By.CSS_SELECTOR,"a.thumb")
    for i in range(len(headline)):
        news.append({
            "id": generate_random_id(),  
            "title": headline[i].text,
            "text": newsdesc[i].text + " |Date:" + daydatetime[i].text,
            "label": 0,  
            "news_url": news_url[i].get_attribute("href"),
            "image": image[i].get_attribute("data-original")
        })

# Convert the news data into a DataFrame
news_df = pd.DataFrame(news)

# Display the DataFrame
st.dataframe(news_df)

# Add a button to download the DataFrame as a CSV file
if st.button('Download CSV'):
    csv = news_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Some strings
    href = f'<a href="data:file/csv;base64,{b64}" download="news_data.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)
