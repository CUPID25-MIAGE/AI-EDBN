from flask import Flask, jsonify, request
import urllib.request
from Bayesian_AI.DevicesCommunication.event_format import event_format
from Bayesian_AI.DevicesCommunication.signals import send_event_signal

app = Flask(__name__)

# HA -> AI
@app.route('/AI/event', methods=['POST'])
def ha_event_handler():
    data = request.get_json()
    event = event_format(data)
    send_event_signal(event)
    return jsonify({'status': 'OK'}), 200

# AI -> HA
def send_request_lamp_on():
    url = "http://localhost:8123/api/webhook/turn_on"
    req = urllib.request.Request(url, method="POST")
    urllib.request.urlopen(req)

def send_request_lamp_off():
    url = "http://localhost:8123/api/webhook/turn_off"
    req = urllib.request.Request(url, method="POST")
    urllib.request.urlopen(req)
