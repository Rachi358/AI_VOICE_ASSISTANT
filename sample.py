import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('voice', engine.getProperty('voices')[0].id)

try:
    engine.say("Hello, this is a test.")
    engine.runAndWait()
except Exception as e:
    print(f"[ERROR] {e}")
