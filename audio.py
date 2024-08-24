from openai import OpenAI
import json
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import time
import keyboard
from pathlib import Path
import num2words
import sys

try:
    client = OpenAI()
except:
    from .secrets.OpenAiKey import key
    client = OpenAI(api_key=key)

class audio:
    def __init__(self, workingFilePath):
        '''
        workingFilePath should be the entire path of the file you want the program to "work" with. This is the one that will be written to and read. It can be anywhere
        '''
        self.workingFilePath = workingFilePath

    def recordAudio(self, recordKey, samplerate=44100):
        defaultInputDevice = sd.default.device[0]
        defaultInputDevice = sd.query_devices(defaultInputDevice)

        chunks = []

        with sd.InputStream(samplerate=samplerate, channels=defaultInputDevice['max_input_channels'], dtype='int16') as stream:
            while not keyboard.is_pressed(recordKey):
                time.sleep(.05)
            while keyboard.is_pressed(recordKey):
                audio_chunk = stream.read(1024)[0]
                chunks.append(audio_chunk)

        if not len(chunks) == 0:
            audio_data = np.concatenate(chunks, axis=0)
            wavfile.write(self.workingFilePath, samplerate, audio_data)
            print(f"Audio saved to {self.workingFilePath}")
        else:
            print(f"no audio recorded, not long enough")
    
    def playAudio(self, interruptKey = None):
        if not interruptKey ==  None:
            keyboard.add_hotkey(interruptKey, sd.stop)

        samplerate, audio_data = wavfile.read(self.workingFilePath)
        sd.play(audio_data, samplerate)
        sd.wait()
    
    def speechToText(self, recordKey) -> str:
        self.recordAudio(recordKey)
        audio_file= open(self.workingFilePath, "rb")
        transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
        )
        return(transcription.text)
    
    def textToSpeech(self, text,  interruptKey = None, voice = "alloy", speed = 1, model = "tts-1"):
        response = client.audio.speech.create(
            model=f"{model}",
            voice=f"{voice}",
            input=f"{text}",
            speed=speed,
            response_format="wav"
        )
        response.stream_to_file(self.workingFilePath)

        self.playAudio(interruptKey)
    
    def convertNumbersToWords(self, text : str):
        # remove all commas seperating numbers
        for i in range(len(text)):
            if i >= len(text):
                break
            elif text[i] == "," and text[i-1].isdigit() and text[i+1].isdigit:
                text = text[:i] + text[i+1:]


        # list that will contain a list of the two pointers denoting where a number is
        numberLocationList = []

        pointer1 = 0
        pointer2 = 0

        while pointer1 < len(text):
            if not text[pointer1].isdigit():
                pointer1+=1
                continue
            pointer2 = pointer1
            while pointer2 <= len(text):
                if pointer2 == len(text)-1:
                    numberLocationList.append([pointer1,pointer2+1])
                    break
                elif text[pointer2].isdigit():
                    pointer2+=1
                    continue
                numberLocationList.append([pointer1,pointer2])
                break
            pointer1=pointer2+1
        
        outputString = ""
        if not len(numberLocationList) == 0:
            for i in range(len(numberLocationList)):
                if i==0:
                    outputString += text[0:numberLocationList[0][0]]
                    if int(text[numberLocationList[0][0]:numberLocationList[0][1]]) < 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000:
                        outputString += num2words.num2words(text[numberLocationList[0][0]:numberLocationList[0][1]])
                    else:
                        number = int(text[numberLocationList[0][0]:numberLocationList[0][1]])
                        exponent = len(str(number)) -1
                        mantissa = int(str(number)[0:5])/(10**4)
                        outputString += f"{num2words.num2words(mantissa)} times ten to the power of {num2words.num2words(exponent)}"
                        
                else:
                    outputString += text[numberLocationList[i-1][1]:numberLocationList[i][0]]
                    if int(text[numberLocationList[i][0]:numberLocationList[i][1]]) < 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000:
                        outputString += num2words.num2words(text[numberLocationList[i][0]:numberLocationList[i][1]])
                    else:
                        number = int(text[numberLocationList[i][0]:numberLocationList[i][1]])
                        exponent = len(str(number)) -1
                        mantissa = int(str(number)[0:5])/(10**4)
                        outputString += f"{num2words.num2words(mantissa)} times ten to the power of {num2words.num2words(exponent)}"
                    

            return(outputString)
        else:
            return(text)