import os
import queue
import sounddevice as sd
import vosk
import json
import numpy as np
import scipy.signal
from datetime import datetime

from HA_communication.Bayesian_AI.Audio.speech_interface import audio_speech_handler  # C’est celle-ci qu’on garde

MODEL_PATH = "/home/pi/Bayesian_AI/vosk-model-small-fr-0.22"
INPUT_SAMPLE_RATE = 48000
TARGET_SAMPLE_RATE = 16000
#AUDIO_DEVICE_NAME = "NewPie: USB Audio"  # A adapter si besoin
CHANNELS = 1

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(f"[Audio error] {status}")
    q.put(indata.copy())

def resample(audio, from_rate, to_rate):
    return scipy.signal.resample_poly(audio, up=to_rate, down=from_rate)

if not os.path.exists(MODEL_PATH):
    print("Modele Vosk non trouve")
    exit(1)

model = vosk.Model(MODEL_PATH)
print("Modele Vosk charge avec succes.")
recognizer = vosk.KaldiRecognizer(model, TARGET_SAMPLE_RATE)

print("Micro pret. Dites 'cupide'...")

#sd.default.device = (AUDIO_DEVICE_NAME, None)
def start_listener():
    print("Micro prêt. Dites 'cupide'...")
    sd.default.device = (None, None)

    with sd.InputStream(samplerate=INPUT_SAMPLE_RATE,
                        channels=CHANNELS,
                        dtype='int16',
                        callback=callback):
        while True:
            data = q.get()
            audio_np = np.frombuffer(data, dtype=np.int16)

            resampled = resample(audio_np, INPUT_SAMPLE_RATE, TARGET_SAMPLE_RATE)
            resampled = resampled.astype(np.int16).tobytes()

            if recognizer.AcceptWaveform(resampled):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower()

                if text:
                    print(f"[Reconnu] {text}")
                    audio_speech_handler(text)
