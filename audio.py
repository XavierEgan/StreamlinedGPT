from openai import OpenAI
import json
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import time
import keyboard
from pathlib import Path
import ffmpeg


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
    
    def textToSpeech(self, text, interruptKey = None):
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=f"{text}",
            response_format="wav"
        )
        response.stream_to_file(self.workingFilePath)

        self.playAudio(interruptKey)
