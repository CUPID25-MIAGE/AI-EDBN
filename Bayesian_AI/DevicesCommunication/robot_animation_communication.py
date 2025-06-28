import serial

PORT = "/dev/ttyACM0"
SER = serial.Serial(PORT, 115200, timeout=1)

def redresser_oreilles():
    SER.write(b'up_both\n')

def oreilles_aleatoires():
    SER.write(b'random_both\n')

def redresser_oreille_gauche():
    SER.write(b'up_left\n')

def redresser_oreille_droite():
    SER.write(b'up_right\n')

def oreilles_aller_retour():
    SER.write(b'back_and_forth_both\n')

def abaisser_oreilles():
    SER.write(b'down_both\n')

def retour_neutre():
    SER.write(b'neutral_both\n')
