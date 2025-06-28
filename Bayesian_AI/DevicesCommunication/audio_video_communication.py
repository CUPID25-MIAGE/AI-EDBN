from signals import send_speech_signal, send_event_signal, send_explanation_requested_signal
from event import Event
from HA_communication.Bayesian_AI.Audio.speech import speak_text

# Matériel -> IA

# Le micro capte des paroles et les envoie à l'IA
def audio_speech_handler(speech):
    if speech.lower() == "cupide explique":
        send_explanation_requested_signal()
        return
    send_speech_signal(speech)

# La caméra capte un évènement et en envoie l'info à l'IA
def video_event_handler(event_name, timestamp):
    event = Event(event_name, timestamp)
    send_event_signal(event)

# Requêtes IA -> Matériel

# Demande de l'IA de prononcer une phrase

def send_request_speak(speech):
    # Appel de la méthode qui va bien dans la partie audio
    speak_text(speech)
    return