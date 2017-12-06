import requests
import urllib.request
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET

def get_rates():
    id_dollar = "R01235"
    id_evro = "R01239"

    valuta = ET.parse(urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req"))

    for  line in valuta.findall('Valute'):
        id_v = line.get('ID')
        if id_v == id_dollar:
            rub = line.find('Value').text
            dollar_rate = "Курс доллара {} рублей".format(rub)
        if id_v == id_evro:
            rub = line.find('Value').text
            euro_rate = "Курс евро {} рублей".format(rub)
    return '\n'.join([dollar_rate, euro_rate])

def get_weather(country="RU", town="Moscow"):
    appid = "9d648aa807674b41c84408b9a8ba7aad"
    s_appid = "&APPID=" + appid
    s_request = "weather?q={},{}&units=metric".format(town, country)
    s_template = "http://api.openweathermap.org/data/2.5/" + s_request + s_appid
    res = requests.get(s_template)
    data = res.json()
    
    formatted = '\n'.join([data['weather'][0]['description']] + ["{}: {}".format(k,v) 
                                                                 for k,v in data['main'].items()])
    return formatted

def get_anekdot():
    resp = urllib.request.urlopen("http://sluchajnoe.ru/anekdot.php")
    soup = BeautifulSoup(resp.read(), "html5lib")
    anek = soup.text.split("\n")[14:15]
    return anek[0].strip()