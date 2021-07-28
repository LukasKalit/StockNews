import requests
import os
import html
import smtplib
from dotenv import load_dotenv
load_dotenv()


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

API_KEY_alphavantage = os.getenv("API_KEY")
API_KEY_news = os.getenv("API_KEY_NEWS")

MAIN_MAIL = os.getenv("MAIN_MAIL")
PASSWORD = os.getenv("PASSWORD")
DESTINATION_MAIL = os.getenv("DESTINATION_MAIL")


formatted_data = []


def send_info():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        print(formatted_data)
        connection.starttls()
        connection.login(MAIN_MAIL, PASSWORD)
        connection.sendmail(MAIN_MAIL,
                            DESTINATION_MAIL,
                            msg=message.encode("utf-8"))


def taking_news():
    global formatted_data
    news_url_params = {
        "apiKey": API_KEY_news,
        "from": list_of_days[0],
        "to": list_of_days[1],
        "qInTitle": COMPANY_NAME,
    }
    news_url = "https://newsapi.org/v2/everything"
    news_request = requests.get(news_url, params=news_url_params)
    news_request.raise_for_status()
    news_data = html.unescape(news_request.json()["articles"])
    formatted_data = [f"Headline: {article['title']}. Brief: {article['description']}" for article in news_data]


stock_url_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_alphavantage,

}
stock_url = 'https://www.alphavantage.co/query'
stock_request = requests.get(stock_url, params=stock_url_params)
stock_request.raise_for_status()
data = stock_request.json()['Time Series (Daily)']

list_of_data = [value for (key, value) in data.items()]
list_of_days = [key for (key, value) in data.items()]
yesterday_data = float(list_of_data[0]["4. close"])
before_yesterday_data = float(list_of_data[1]["4. close"])
rise_fall_data = round(yesterday_data/before_yesterday_data/100, 2)


if yesterday_data/before_yesterday_data-1 > 0.00:
    taking_news()
    message = f"Subject:TSLD: 🔺{rise_fall_data}%\n\n{formatted_data}"
    print(message)
    send_info()

elif yesterday_data/before_yesterday_data-1 < -0.00:
    taking_news()
    message = f"Subject:TSLD: 🔻{rise_fall_data}%\n\n{formatted_data}"
    print(message)
    send_info()

else:
    print(round(yesterday_data/before_yesterday_data/100, 2))
    print("nothing special happened with TSLA stock")
