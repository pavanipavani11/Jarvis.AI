import speech_recognition as sr
import pyttsx3
import openai
import datetime
import webbrowser
import os
import requests

# ✅ API Keys
openai.api_key = "YOUR_OPENAI_API_KEY"
weather_api_key = "YOUR_OPENWEATHER_API_KEY"

# ✅ Text-to-Speech Setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Jarvis. How can I assist you today?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
    except Exception:
        speak("Sorry, I didn't catch that. Could you repeat?")
        return "None"
    return command.lower()

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': weather_api_key,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data["cod"] != "404":
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"The current temperature in {city} is {temp} degrees Celsius with {description}."
        else:
            return "City not found."
    except Exception:
        return "I couldn't fetch the weather right now."

def chat_with_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def perform_task(command):
    if 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")

    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {current_time}")

    elif 'set reminder' in command:
        speak("What should I remind you about?")
        reminder = take_command()
        with open("reminder.txt", "w") as f:
            f.write(reminder)
        speak("Reminder saved.")

    elif 'show reminder' in command:
        try:
            with open("reminder.txt", "r") as f:
                reminder = f.read()
            speak(f"Your reminder is: {reminder}")
        except:
            speak("No reminder found.")

    elif 'weather in' in command:
        city = command.split("in")[-1].strip()
        weather_info = get_weather(city)
        speak(weather_info)

    else:
        response = chat_with_openai(command)
        speak(response)

# ✅ Main
if __name__ == "__main__":
    wish_user()
    while True:
        command = take_command()
        if command == "none":
            continue
        elif 'exit' in command or 'stop' in command:
            speak("Goodbye!")
            break
        else:
            perform_task(command)
