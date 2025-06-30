import sys
import os
import threading
from DevicesCommunication.rest_communication import app
from Audio.listener2 import start_listener
from Video.hailo_rpi5_examples.basic_pipelines.detection3 import start_detection
from Bayesian_AI.DevicesCommunication.rest_communication import launch_server

sys.path.append('/home/pi/Bayesian_AI/Video/hailo_rpi5_examples/venv_hailo_rpi5_examples/lib/python3.11/site-packages')

if __name__ == '__main__':
    # Chemins des fichiers YOLO
    hef_path = os.path.join("Video", "yolo", "family.hef")
    label_path = os.path.join("Video", "yolo", "my-labels.json")

    # Demarrer la detection video dans un thread
    detection_thread = threading.Thread(
        target=start_detection,
        args=(hef_path, label_path),
        daemon=True
    )
    detection_thread.start()

    # Demarrer l'ecoute audio
    listener_thread = threading.Thread(target=start_listener, daemon=True)
    listener_thread.start()

    # Lancer le serveur http local
    http_thread = threading.Thread(target=launch_server)
    http_thread.start()

    # TODO : Lancer le processus central de l'IA (hors d'un thread)

