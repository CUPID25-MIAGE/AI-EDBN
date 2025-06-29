from re import split

from DevicesCommunication.signals import EVENT_SIGNAL, SPEECH_SIGNAL, EXPLANATION_SIGNAL
from helper import add_new_row_csv
from Bayesian_AI.DevicesCommunication.requests import *
from datetime import datetime


# Possible de tester en exécutant le main et avec la commande suivante qui imite un message envoyé depuis HA:
# curl -X POST http://localhost:8080/AI/event
# -H "Content-Type: application/json"
# -d '{"entity": "light", "old_state": "off", "new_state": "on", "time": "2025-05-17T18:20:56.700000"}'
def HA_event_method(event):
    if event.name == "sunUp":
        from helper import sun_up
        sun_up()
    elif event.name == "sunDown":
        from helper import sun_down
        sun_down()
    add_new_row_csv([event.name, event.timestamp])
    print(event.name)
    print(event.timestamp)

# En attente de méthode pour tester ca
def speech_signal(speech):
    speech = speech.lower()
    base_sentence = "cupide"
    timestamp = datetime.now().astimezone().isoformat()

    # execute the command based on the speech input
    if speech == base_sentence+ " ouvre les volets":
        request_shutter_open()
        add_new_row_csv([timestamp,"shutter_open"])
    elif speech == base_sentence+ " ferme les volets":
        request_shutter_close()
        add_new_row_csv([timestamp, "shutter_close"])
    elif speech == base_sentence+ " allume la musique":
        request_music_on()
        add_new_row_csv([timestamp, "music_on"])
    elif speech == base_sentence+ " éteint la musique":
        request_music_off()
        add_new_row_csv([timestamp, "music_off"])

    # execute the command and learn the pattern
    elif speech == base_sentence+ " souviens-toi allume la lumière":
        request_lamp_on()
        add_new_row_csv([timestamp, "lamp_on"])
        train_model_on("lamp_on")
    elif speech == base_sentence+ " souviens-toi éteint la lumière":
        request_lamp_off()
        add_new_row_csv([timestamp, "lamp_off"])
        train_model_on("lamp_off")
    elif speech == base_sentence+ " souviens-toi ouvre les volets":
        request_shutter_open()
        add_new_row_csv([timestamp, "shutter_open"])
        train_model_on("shutter_open")
    elif speech == base_sentence+ " souviens-toi ferme les volets":
        request_shutter_close()
        add_new_row_csv([timestamp, "shutter_close"])
        train_model_on("shutter_close")
    elif speech == base_sentence+ " souviens-toi allume la musique":
        request_music_on()
        add_new_row_csv([timestamp, "music_on"])
        train_model_on("music_on")
    elif speech == base_sentence+ " souviens-toi éteint la musique":
        request_music_off()
        add_new_row_csv([timestamp, "music_off"])
        train_model_on("music_off")

    else :
        request_speak("Je n'ai pas compris la commande. Veuillez réessayer. NYAH!")
    return

# En attente de méthode pour tester ca
def test_explanation_signal():
    print("Explication en cours")

EVENT_SIGNAL.connect(HA_event_method)
SPEECH_SIGNAL.connect(speech_signal)
EXPLANATION_SIGNAL.connect(test_explanation_signal)