import requests
from twilio.rest import Client

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ACCOUNT_SID = 'AC32c08e87906339e65fa95fc3ee4d124e'
AUTH_TOKEN = "dfb4c4ceb08e68486393e891d4eacac0"


para={
    "function":"TIME_SERIES_DAILY",
    "symbol":"RELIANCE.BSE",
    "outputsize":"full:",
    "apikey":"FBIDA6AMPNJ6G0BF"
}

response = requests.get(STOCK_ENDPOINT, params=para)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

data_diff = abs(float(yesterday_closing_price)-float(day_before_yesterday_closing_price))

up_down = None
if data_diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
diff_per = (data_diff/float(yesterday_closing_price)) * 100

if diff_per > 0.0005:
    print("a")
    para={
        "qInTitle" : "RELIANCE",
        "apiKey" : "1f9d0c886aa044dc8aa56c62f60e4857"
    }
    response_from_news = requests.get(NEWS_ENDPOINT, params=para)
    artical = response_from_news.json()["articles"]
    three_at = artical[:3]


    formatted_articles = [f"RELIANCE:{up_down}{diff_per}% \n Headline: {article['title']}. \n Brief: {article['description']}" for article in three_at]
    print(formatted_articles)
    client = Client(ACCOUNT_SID,AUTH_TOKEN)
    for articale in formatted_articles:
        message = client.messages.create(
            body=articale,
            from_="+13132511766",
            to="+919429686999"
        )
