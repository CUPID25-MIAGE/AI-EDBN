import serial

PORT = "/dev/ttyACM0"
SER = serial.Serial(PORT, 115200, timeout=1)

def close_shutter():
    SER.write(b'close_shutter\n')

def open_shutter():
    SER.write(b'open_shutter\n')
