from DevicesCommunication.signals import EVENT_SIGNAL, SPEECH_SIGNAL, EXPLANATION_SIGNAL
from helper import add_new_row_csv


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
def test_speech_signal(speech):
    print(speech)

# En attente de méthode pour tester ca
def test_explanation_signal():
    print("Explication en cours")

EVENT_SIGNAL.connect(HA_event_method)
SPEECH_SIGNAL.connect(test_speech_signal)
EXPLANATION_SIGNAL.connect(test_explanation_signal)