#recinhecimento do google para quando estivermos online e vosk para reconhecimento offline
from vosk import Model, KaldiRecognizer
import os

import core
import pyaudio
import pyttsx3

import json


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()


model = Model("model")
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, input=True, rate = 16000, frames_per_buffer=2048)
stream.start_stream()


while True:
    data = stream.read(2048)
    if len(data) == 0:
        break

    if rec.AcceptWaveform(data):
        result = rec.Result()
        result = json.loads(result)


        if result is not None:
            text = result['text']

            print(text)
            if text == 'que horas são' or text == 'diga as horas' or text =='horas por favor' :
                speak(core.Systeminfo.get_time())
        

    



