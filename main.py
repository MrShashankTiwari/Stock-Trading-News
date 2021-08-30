import requests
import smtplib
from datetime import date, timedelta

today = date.today()
yesterdate = today - timedelta(days=1)
YESTERDAY = yesterdate.strftime('%Y-%m-%d')

date_before1 = today - timedelta(days=2)
DAY_BEFORE = date_before1.strftime('%Y-%m-%d')

my_email = YOUR EMAIL
my_password = YOUR PASSWORD

STOCK_NAME = INTERESTED STOCK NAME
COMPANY_NAME = "STOCK (COUNTRY - STOCK EXCHANGE)"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

API_KEY_ALPHA = os.environ["API_KEY_FROM_ALPHAVANTAGE"]
API_KEY_NEWS = os.environ["API_KEY_FROM_NEWSAPI"]

parameters_stock = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": {STOCK_NAME},
    "apikey": {API_KEY_ALPHA}
}

parameters_news = {
    "apiKey": API_KEY_NEWS,
    "q": "STOCK_NAME",
    "from": DAY_BEFORE,
    "to": YESTERDAY,
    "language": "en",
    "sortBy": "publishedAt",
}

response_stock = requests.get(
    url=STOCK_ENDPOINT, params=parameters_stock)
response_stock.raise_for_status()
data = response_stock.json()

yesterday_closing = float(data['Time Series (Daily)'][YESTERDAY]['4. close'])
day_before_closing = float(data['Time Series (Daily)'][DAY_BEFORE]['4. close'])

difference = abs(yesterday_closing - day_before_closing)
percent_diff = round((difference/yesterday_closing)*100, 3)

if percent_diff > 0.01:
    response_news = requests.get(
        url=NEWS_ENDPOINT, params=parameters_news)
    response_news.raise_for_status()
    news_data = response_news.json()
    news_list = news_data["articles"][0:3]
    descriptions = [news_list[item]["description"]
                    for item in range(len(news_list))]
    link = [news_list[item]["url"]
            for item in range(len(news_list))]
    for i in range(0, 3):
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email,
                            msg=f"Subject:STOCK_NAME changes by {percent_diff}!!\n\n{descriptions[i]}\n{link[i]}")
