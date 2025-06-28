from DevicesCommunication.signals import send_speech_signal, send_explanation_requested_signal
from Audio.speech import speak_text

# Fonction appelee depuis le listener apres reconnaissance vocale
def audio_speech_handler(speech):
    speech = speech.lower()
    if speech == "cupide explique":
        send_explanation_requested_signal()
    elif speech.startswith("cupide "):
        # Commence bien par "cupide " mais pas "cupide explique"
        send_speech_signal(speech)
    else:
        # Ne rien faire sinon
        pass


# Fonction appellee par l'IA quand elle veut parler
def send_request_speak(speech):
    speak_text(speech)
