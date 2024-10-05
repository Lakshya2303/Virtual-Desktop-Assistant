import os
import subprocess as sp
import pyttsx3
import speech_recognition as sr
import keyboard
from datetime import datetime
from decouple import config
from conv import random_text
from random import choice
from online import find_my_ip, search_on_wikipedia, search_on_google, weather_forecast
import requests
import wolframalpha

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

USER = config('USER')
HOSTNAME = config('BOT')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_me():
    hour = datetime.now().hour
    if (hour>=6) and (hour<12):
        speak(f"Good morning {USER}")
    elif (hour>=12) and (hour<=16):
        speak(f"Good afternoon {USER}")
    elif (hour>=16) and (hour<19):
        speak(f"Good evening {USER}")
    speak(f"I am {HOSTNAME}. How may I assist you {USER}?")

listening = False

def start_listening():
    global listening
    listening = True
    print("Started listening")

def pause_listening():
    global listening
    listening = False
    print("Stopped listening")

keyboard.add_hotkey("ctrl+alt+k", start_listening)
keyboard.add_hotkey("ctrl+alt+p", pause_listening)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)
        if not 'stop' in query or 'exit' in query:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour>=21 and hour<6:
                speak("Good Night SIR, take care!")
            else:
                speak("Have a good day SIR!")
            exit()

    except Exception:
        speak("Sorry i couldn't understand. Can you please repeat that?")
        query = 'None'
    return query

if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I am absolutely fine SIR. What about you")

            elif "open command prompt" in query:
                speak("Opening command prompt SIR")
                os.system("start cmd")

            elif "open spotify" in query:
                speak("Opening Spotify SIR")
                spotify_path = "C:\\Users\\khims\\OneDrive\\Desktop\\Spotify.lnk"
                os.startfile(spotify_path)

            elif "open whatsapp" in query:
                speak("Opening Whatsapp SIR")
                whatsapp_path = "https://web.whatsapp.com/"
                os.startfile(whatsapp_path)

            elif "open youtube" in query:
                speak("Opening YouTube SIR")
                youtube_path = "https://youtube.com/"
                os.startfile(youtube_path)

            elif "open vs code" in query:
                speak("Opening VS CODE SIR")
                vscode_path = "C:\\Users\\khims\\OneDrive\\Desktop\\Visual Studio Code.lnk"
                os.startfile(vscode_path)

            elif "Google" in query:
                speak(f"what do you want to search on Google {USER}")
                query = take_command().lower()
                search_on_google(query)

            elif "Wikipedia" in query:
                speak(f"What do you want to search on Wikipedia {USER}")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to Wikipedia, {results}")
                print(results)

            elif "weather" in query:
                ip_address = find_my_ip()
                city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
                speak(f"Getting weather report of your city {city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                speak(f"Also the weather report talks about {weather}")

            elif "calculator" in query:
                app_id = "53GELA-VYKRV65YKT"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query("".join(text))
                try:
                    ans = next(result.results).text
                    speak("The answer is "+ans)
                except StopIteration:
                    speak("I couldn't find that. Please try again")

