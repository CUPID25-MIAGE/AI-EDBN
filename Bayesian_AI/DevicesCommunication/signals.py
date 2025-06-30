# DevicesCommunication/signals.py

from blinker import Signal

# Signaux partages
EVENT_SIGNAL = Signal("event")
SPEECH_SIGNAL = Signal("speech")
EXPLANATION_SIGNAL = Signal("explanation")

def send_event_signal(event):
    print("[Signal] EVENT_SIGNAL envoye")
    EVENT_SIGNAL.send(event)

def send_speech_signal(speech):
    print("[Signal] SPEECH_SIGNAL envoye")
    SPEECH_SIGNAL.send(speech)

def send_explanation_requested_signal():
    print("[Signal] EXPLANATION_SIGNAL envoye")
    EXPLANATION_SIGNAL.send()

