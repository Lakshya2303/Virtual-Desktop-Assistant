from ipaddress import ip_address

import requests
import wikipedia
import pywhatkit as kit

def find_my_ip():
    ip_address = requests.get("https://api.ipify.org?format=json").json
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=3)
    return results

def search_on_google(query):
    kit.search(query)

def weather_forecast(city):
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=46b6a953d6b483dab7cdba69e34ae36b").json()
    weather  = res["weather"][0]["main"]
    temp = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather,f"{temp} C",f"{feels_like} C"