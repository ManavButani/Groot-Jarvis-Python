from urllib import request
import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib
import pyaudio
import pandas as pd

# for location
import requests
import json


"""                             
"                                                  Project title : Groot
                                            Front-end: Python  Back-end: Python
Is a software like Google assistant , Apple siri and have functionality of mail, Play music , study on onother websites and so more."

"""
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
# print(voices[1].id)
engine.setProperty("voice", voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Student Assistant Sir. Please tell me how may I help you")


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("youremail@gmail.com", "your-password")
    server.sendmail("youremail@gmail.com", to, content)
    server.close()


if __name__ == "__main__":
    wishMe()
    while True:
        # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "website" in query:
            df = pd.read_csv("website_url.csv")
            given_domain = query.replace("open website", "")
            result = df[df["domain"] == given_domain.lower().replace(" ", "")][
                "domain_url"
            ].values
            if len(result) > 0:
                domain_url = result[0]
                webbrowser.open(domain_url)
            else:
                print(f"No URL found for {given_domain}")


        elif "play music" in query:
            music_dir = "E:\\vandu katha\\Bhagvat Gita Sanskrit"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif "open code" in query:
            codePath = "C:\\Program Files\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif "study material" in query:
            studyPath = "D:\\5th sem\\www.w3schools.com\\python\\default.html"
            os.startfile(studyPath)

        elif "mail to user" in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "19it016@charusat.edu.in"
                sendEmail(to, content)
                speak("Gmail has been sent!")
            except Exception as e:
                print(e)
                speak("my friend , I am not able to send")

        elif "current location" in query or "1" in query:
            speak("wait sir, let me check")
            try:
                ipAdd = requests.get("https://api.ipify.org").text
                print(ipAdd)
                url = "https://get.geojs.io/v1/ip/geo/" + ipAdd + ".json"
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                city = geo_data["city"]
                country = geo_data["country"]
                speak(f"we are in a {city} city of {country}")
            except Exception as e:
                speak("Due to network issue i am unable to find location")

        elif "turn off" in query:
            speak("Ok sir, I am !")
            exit()
