# Video/signal_handlers.py

from Bayesian_AI.DevicesCommunication.signals import EVENT_SIGNAL, EXPLANATION_SIGNAL
from Bayesian_AI.Audio.speech import speak_text

# Handler pour l'evenement "nico"
def handle_event(message):
    print("[EVENT_SIGNAL] Evenement capte")
    if message == "nico=true":
        print("[EVENT_SIGNAL] Nico detecte OK")
    elif message == "nico=false":
        print("[EVENT_SIGNAL] Nico non detecte KO")

# Connexion du handler a EVENT_SIGNAL
EVENT_SIGNAL.connect(handle_event)
print("[Video] En attente d'evenements 'nico=true/false' via EVENT_SIGNAL...")

# Handler pour l'explication
def explanation_handler(_=None):
    print("[EXPLANATION_SIGNAL] Signal recu")
    speak_text("Voici l'explication que vous avez demandee. Je suis le plus mignon de tous les lapins sur Terre !")

# Connexion du handler a EXPLANATION_SIGNAL
EXPLANATION_SIGNAL.connect(explanation_handler)
print("[Video] En attente du signal 'EXPLANATION_SIGNAL'... (Lance listener.py et dis 'cupide explique')")
