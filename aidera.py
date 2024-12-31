import speech_recognition as sr
import pyttsx3
from vosk import Model, KaldiRecognizer
import pyaudio
import datetime
import webbrowser

engine = pyttsx3.init()
model = Model('vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15')
recognizer = KaldiRecognizer(model,16000)

voices = engine.getProperty('voices')
# engine.setProperty(voices[0])


def speak(message):
    engine.say(message)
    engine.runAndWait()

def commands():
    
    p = pyaudio.PyAudio()
    streaming = p.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=8000)
    print("Listening....")
    streaming.start_stream()
    
    while True:
        data = streaming.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = eval(result) 
            query = result_dict.get("text", "").lower()
            print(f"You said: {query}")
            return query
    return ""


def response_command(query):

    if 'hello' in query:
        speak("Hi There! How are you?")
    elif 'time' in query:
        curr_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time right now is {curr_time}")
    elif 'open' in query:
        replace = query.replace("open ","")
        webbrowser.open(f"https://www.{replace}.com")
        speak(f"Opening {replace}")
    elif 'stop' or 'exit' in query:
        speak('Goodbye')
        exit()
    
    else:
        speak("I am not sure how to respond for that.")
        


def main():
    speak("Hello. Myself Aidera, your virtual assistance. How can I help you?")
    while True:
        query = commands()
        response_command(query)

if __name__ == "__main__":
    main()