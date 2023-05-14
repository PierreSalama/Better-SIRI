import openai
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import simpledialog

openai.organization = "ur organization token"
openai.api_key = "ur token"

r = sr.Recognizer()
previous_question = ""

def voice_input():
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None

def text_input():
    root = tk.Tk()
    root.withdraw()
    input_text = simpledialog.askstring("Text Input", "Enter text:", parent=root)
    root.destroy()
    return input_text

def openai_response(prompt):
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=200)
    return response['choices'][0]['text']

def show_response(response):
    root = tk.Tk()
    root.withdraw()
    simpledialog.messagebox.showinfo("Response from OpenAI", response, parent=root)
    root.destroy()

def tts_response(response):
    engine = pyttsx3.init()
    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 200)
    engine.say(response)
    engine.runAndWait()

while True:
    root = tk.Tk()
    root.withdraw()
    input_method = simpledialog.askinteger("Input Method", "Enter 1 for voice input or 2 for text input:", minvalue=1, maxvalue=2, parent=root)
    root.destroy()
    if input_method == 1:
        text = voice_input()
        if text:
            if previous_question:
                prompt = previous_question + " " + text
            else:
                prompt = text
            response = openai_response(prompt)
            show_response(response)
            tts_response(response)
            previous_question = text
    else:
        text = text_input()
        if text:
            if previous_question:
                prompt = previous_question + " " + text
            else:
                prompt = text
            response = openai_response(prompt)
            show_response(response)
            tts_response(response)
            previous_question = text
