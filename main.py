import pyaudio
import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit as pwk
import mtranslate
import gemini_request
from gemini_request import generate_from_gemini, send_request2
import user_config
from wakeUp import listen_for_wake_word
import warnings
warnings.filterwarnings("ignore")

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)
engine.setProperty('rate', 180)

def speak(text):
    try:
        print(f"AI: {text}")
        engine.say(text)
        # translated = mtranslate.translate(text, "hi", "en-in")
        # engine.say(translated)
        engine.runAndWait()
    except Exception as e:
        print(f"[Voice Error] {e}")

def command():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language='en-in')
                print(f"You: {query}")
                return query.lower()
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand.")
            except sr.RequestError:
                print("Request error. Check your internet connection.")
    except OSError:
        print("[ERROR] Microphone not found.")
    return ""

def main_process():
    ara_chat = []
    while True:
        listen_for_wake_word()
        speak("Yes, how can I help you?")
        request = command()
        if not request:
            continue

        if "hello" in request:
            speak("Hello, I am Yara. How can I help you?")

        elif any(phrase in request for phrase in ["play music", "can you play music", "start music"]):
            speak("Playing music")
            links = [
                "https://youtu.be/ycS5PagXvhQ?si=eydAuh41dqH0gIVI",
                "https://youtu.be/SxTYjptEzZs?si=BRTzaX7bNegqIp2Z",
                "https://youtu.be/K6WyEgsSYv8?si=1cxZkHfZNMD5bjYv",
                "https://youtu.be/AtnB0DbuFFU?si=Ki1wkgJxmo3eF1sF",
                "https://youtu.be/Gqy01K0wQ_k?si=IDfZH-vEQ41mXsi7"
            ]
            webbrowser.open(random.choice(links))

        elif "say time" in request:
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak(f"The current time is {current_time}")

        elif "say date" in request:
            todays_date = datetime.datetime.now().strftime("%d:%m:%Y")
            speak(f"Today's date is {todays_date}")

        elif "new task" in request:
            task = request.replace("new task", "").strip()
            if task:
                speak(f"Adding {task} to your to-do list")
                with open("todo.txt", "a") as file:
                    file.write(task + "\n")

        elif "speak task" in request:
            try:
                with open("todo.txt", "r") as file:
                    speak("Here are your tasks: " + file.read())
            except FileNotFoundError:
                speak("No tasks found.")

        elif "show task" in request:
            try:
                with open("todo.txt", "r") as file:
                    tasks = file.readlines()
                    notification.notify(
                        title="Your Tasks",
                        message=''.join(tasks),
                        app_name="Task Manager",
                        timeout=20
                    )
                    for i, task in enumerate(tasks, 1):
                        print(f"Task {i}: {task.strip()}")
            except FileNotFoundError:
                speak("No tasks to show.")

        elif "open youtube" in request:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open" in request:
            app = request.replace("open", "").strip()
            pyautogui.press("super")
            pyautogui.typewrite(app)
            pyautogui.sleep(2)
            pyautogui.press("enter")

        elif "wikipedia" in request:
            topic = request.replace("search on wikipedia", "").strip()
            if topic:
                try:
                    speak("Searching Wikipedia...")
                    summary = wikipedia.summary(topic, sentences=2)
                    print(summary)
                    speak(summary)
                except wikipedia.exceptions.DisambiguationError:
                    speak("Be more specific, there are many results.")
                except wikipedia.exceptions.PageError:
                    speak("No results found on Wikipedia.")

        elif "google" in request:
            topic = request.replace("search on google", "").strip()
            if topic:
                speak(f"Searching Google for {topic}")
                webbrowser.open(f"https://www.google.com/search?q={topic}")

        elif "send message" in request:
            pwk.sendwhatmsg_to_group_instantly("Major project", "Hello from Rachit")

        elif "ask ai" in request:
            query = request.replace("ask ai", "").strip()
            response = generate_from_gemini(query)
            if response:
                print(response)
                speak(response)
            else:
                speak("Couldn't get a response from AI.")

        elif "clear chat" in request:
            ara_chat.clear()
            speak("Chat cleared.")

        elif "jimmy" in request:
            message = request.replace("jimmy", "").strip()
            ara_chat.append({"role": "user", "content": message})
            response2 = send_request2(ara_chat)
            if response2:
                ara_chat.append({"role": "assistant", "content": response2})
                speak(response2)
            else:
                speak("Couldn't get a response from AI.")

        elif "bye" in request:
            speak("Goodbye!")
            break

        else:
            speak("I didn't understand that command. Please try again.")

if __name__ == "__main__":
    main_process()
