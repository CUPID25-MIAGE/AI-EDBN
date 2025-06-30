from Bayesian_AI.Audio.speech_interface import send_request_speak
from Bayesian_AI.Audio.music import launch_music, stop_music
from rest_communication import send_request_lamp_on, send_request_lamp_off
from robot_animation_communication import *
from shutter_communication import open_shutter, close_shutter


# Lampe
def request_lamp_on():
    send_request_lamp_on()

def request_lamp_off():
    send_request_lamp_off()

# Text to Speech
def request_speak(speech):
    send_request_speak(speech)

# Mouvement des oreilles 
def request_ears_up():
    redresser_oreilles()

def request_ears_random():
    oreilles_aleatoires()

def request_left_ear_up():
    redresser_oreille_gauche()

def request_right_ear_up():
    redresser_oreille_droite()

def request_ears_back_and_forth():
    oreilles_aller_retour()

def request_ears_down():
    abaisser_oreilles()

def request_ears_neutral():
    retour_neutre()

# Mouvement du moteur (volet)

def request_shutter_open():
    open_shutter()

def request_shutter_close():
    close_shutter()

def request_music_on():
    launch_music()

def request_music_off():
    stop_music()

# Rougir (Non implémenté)
def request_blush():
    return

