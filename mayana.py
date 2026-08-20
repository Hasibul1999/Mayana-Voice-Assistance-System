import speech_recognition as sr
import pyttsx3
import logging
import os
import datetime
import wikipedia
import webbrowser
import random
import subprocess
import google.generativeai as genai

# Logging configuration

LOG_DIR = "Logs"
LOG_FILE_NAME = "logs_data.log"

os.makedirs(LOG_DIR,exist_ok=True)

filepath = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=filepath,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level= logging.INFO
)

#Activating voice

engine = pyttsx3.init("sapi5")
engine.setProperty("rate",170)
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)

def speak(text):
    """This function takes texts and pronounce them

    Arg = text
    return = voice
    """
    engine.say(text)
    engine.runAndWait()


# This function recognise the speech

def takeCommand():
    """Convert voices into query
    
    return instruction as text
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognising......")
        instruction = r.recognize_google(audio, language='en-in')
        print(f"You said: {instruction}\n")
        return instruction

    except Exception as e:
        logging.info(e)
        #print("Would you repeat please?")
        return "None"

def greeting():
    hour = datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Good Morning, sir. How are you doing?")    
    elif hour>=12 and hour<18: 
        speak("Good afternoon, sir. How are you doing?")
    else:
        speak("Good evening, sir. How are you doing?")

    speak("I am Mayana. How may I help you today?")

def playmusic():
    music = "E:\\InceptionBD_Classes\\Mayana-Voice-Assistance-System\\Musics"
    try:
        songs = os.listdir(music)
        if songs:
            rand_song = random.choice(songs)
            os.startfile(os.path.join(music,rand_song))
        else:
            speak("No music found.")
    except Exception as e:
        speak("Music cannot be played.")
        logging.info(e)

def ai_model_response(user_input):
    GEMINI_API_KEY = ".................."
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-3.6-flash")
    prompt = f"Suppose you are Mayana, an AI assistant. Answer the provided question within 4 sentences, Question: {user_input}"
    response = model.generate_content(prompt)
    result = response.text
    return result


greeting()
JOKES = ["Teacher: Why are you late?\nStudent: Because of the sign.\nTeacher: What sign? \nStudent: School Ahead, Go Slow. 😄",
     "Friend: Why are you talking to your computer?\nMe: It asked me to press any key.\nFriend: So?\nMe: I couldn't find the Any key. 😂",
     "Mom: Why is your room so messy?\n Me: I'm an organized person.\n Mom: Then organize it!\nMe: It's organized chaos. 😎"]

while True:
    instruction = takeCommand().lower()
    print(instruction)
    speak(instruction) 

    if "your name" in instruction:
        speak("My name is Mayana")

    elif "time" in instruction:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        logging.info("user asked for the time.")
        speak(f"The time is: {time}")

    elif "thank you" in instruction:
        speak("You are welcome. I am happy to help you.")

    elif "open google" in instruction:
        speak("okay sir. Google is being opened")
        logging.info("Opened google.")
        webbrowser.open("google.com")

    elif "calculator" in instruction:
        speak("okay sir. Calculator is being opened")
        logging.info("Opened calculator.")
        subprocess.Popen("calc.exe")
        

    elif "notepad" in instruction:
        speak("okay sir. Notepad is being opened")
        logging.info("Opened notepad.")
        subprocess.Popen("notepad.exe")
        

    elif "term" in instruction or "terminal" in instruction:
        speak("okay sir. terminal is being opened")
        logging.info("Opened terminal.")
        subprocess.Popen(["cmd.exe"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        

    elif "youtube" in instruction:
        speak("okay sir. youtube is being opened")
        query = instruction.replace("youtube","")
        logging.info("Opened YouTube.")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    elif "github" in instruction:
        speak("okay sir. github is being opened")
        logging.info("Opened Github")
        webbrowser.open("https://github.com/")

    # elif "wikipedia" in instruction:
    #     speak("okay sir. Wikipedia is being opened")
    #     query = instruction.replace("wikipedia","")
    #     webbrowser.open(f"https://en.wikipedia.org/wiki/{query}")

    elif "joke" in instruction:
        speak("Here is a joke.")
        logging.info("Asked for a joke.")
        speak(random.choice(JOKES))

    elif "music" in instruction:
        speak("Here is a music for you.")
        playmusic()

    elif "wikipedia" in instruction:
        speak("Searching in wikipedia")
        query = instruction.replace("wikipedia","")
        result = wikipedia.summary(query,sentences=2)
        speak("According to wikipedia")
        speak(result)
        logging.info("User searched something from wikipedia.")

    elif "exit" in instruction:
        speak("Okay, sir. Thank you for your time. Have a good day.")
        logging.info("user asked to exit from the program.")
        exit() 

    elif "you eat" in instruction:
        speak("I am machine. I eat electricity.")
    

    else:
        print("Conducting AI search")
        res = ai_model_response(instruction)
        speak(res)
        logging.info("user asked for miscellaneous questions.")
    