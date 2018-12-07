from urllib.parse import urljoin
import requests
from django.conf import settings

BASE_URL = "https://api.openweathermap.org/data/2.5/"

def get_weather(city):
    weather_url = 'weather?q=%s&APPID=%s' %(city, settings.OWP_API_KEY)
    url = urljoin(BASE_URL, weather_url)
    response = requests.get(url)
    return response

def get_weather_time(city):
    forecat_time_url = 'forecast?q=%s&APPID=%s' %(city, settings.OWP_API_KEY)
    url = urljoin(BASE_URL, forecat_time_url)
    response = requests.get(url)
    return response