import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime, timezone
import pytz, random, os

TelegramApi = 'https://api.telegram.org/bot'
TelegramBotToken = os.environ.get("TELEGRAM_API_TOKEN")

my_dict = {
    "https://www.mident.cz": "/kontakttest",
    "https://www.mident.ro": "/contact",
    "https://www.midentcare.hu": "/contact",
    "https://www.mident-de.de": "https://www.mident-de.de/kontakt/",
    "https://www.jansel.cz": "/kontakt",
    "https://www.nakupino.cz": "/kontakt",
    "https://www.purplpink.cz": "https://purplpink.cz/kontakt/"
}

def check_website(url, link):
    proxies = [
    {'http': '198.59.191.234:8080'},
    {'http': '92.118.232.74:8080'},
    {'http': '174.70.1.210:8080'}
]

    user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Android 12; Mobile; rv:85.0) Gecko/85.0 Firefox/85.0",
    "Mozilla/5.0 (Android 13; Mobile; rv:85.0) Gecko/85.0 Firefox/85.0",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/89.0.4389.82 Mobile/16E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/89.0.4389.82 Mobile/15E148 Safari/604.1",
]

    headers = {
        'User-Agent': random.choice(user_agents)
}

    proxy = random.choice(proxies)

    r = requests.get(url, headers=headers, proxies=proxy)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        if soup.find('a', href=link):
            return True
        else:
            return False
    else:
        return False

def send_message(chat_id, message):
    
    # Set the parameters for the message
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode':'HTML',
        'disable_web_page_preview': True
    }

    # Send the request to the API endpoint
    response = requests.get(f'{TelegramApi}{TelegramBotToken}/sendMessage', params=params)
    
    # Return the response from the API
    return response.json()

def get_domain_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
       domain = domain[4:]
       domain = "<a href=\"https://www." + domain + "\">" + domain + "</a>"
    return domain

def get_prague_time():
    tz = pytz.timezone('Europe/Prague')
    prague_time = datetime.now(tz)
    return prague_time.strftime('%d/%m/%Y %H:%M')

message = "<b>Website uptime info</b>:\n"
message += get_prague_time() + "\n"
check_failed = False
# Iterate over the dictionary
for key, value in my_dict.items():
    message += get_domain_name(key) + ": "
    start = datetime.now()
    if check_website(key, value):
       message += "(\U0001F7E2)"
    else:
       message += "(\U0001F534)"
       check_failed = True
    end = datetime.now()
    elapsed = end - start
    elapsed_seconds = elapsed.total_seconds()
    #seconds_with_one_decimal = formatted_time[:2]
    message += " (" + f"{elapsed_seconds:.2f}" + "S)\n"

if (check_failed):
    send_message(os.environ.get("TELEGRAM_CHAT_ID"), message)
