import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import os
import numpy as np
import cv2
import hailo

from DevicesCommunication.signals import send_event_signal
from event import Event


from hailo_apps_infra.hailo_rpi_common import (
    get_caps_from_pad,
    get_numpy_from_buffer,
    app_callback_class,
)
from hailo_apps_infra.detection_pipeline import GStreamerDetectionApp

import csv
from datetime import datetime

# Fichier de log CSV (il sera ecrase a chaque lancement, sauf si tu changes le mode)
CSV_LOG_PATH = "/home/pi/event_log.csv"

# Initialiser le fichier avec l'entete si besoin
if not os.path.exists(CSV_LOG_PATH):
    with open(CSV_LOG_PATH, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["case_id", "timestamp", "event", "person1_detected", "person2_detected", "person3_detected", "nico_detected"])

# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
class user_app_callback_class(app_callback_class):
    def __init__(self):
        super().__init__()
        self.new_variable = 42  # New variable example
        self.previous_detection = {  # Initial states of each person
            "person1": False,
            "person2": False,
            "person3": False,
            "nico": False
        }

    def new_function(self):  # New function example
        return "The meaning of life is: "

# -----------------------------------------------------------------------------------------------
# User-defined callback function
# -----------------------------------------------------------------------------------------------
def app_callback(pad, info, user_data):
    # Get the GstBuffer from the probe info
    buffer = info.get_buffer()
    # Check if the buffer is valid
    if buffer is None:
        return Gst.PadProbeReturn.OK
        
    # Incrément du compteur dès qu'un buffer valide est reçu
    user_data.increment()
    # Ne traiter qu'une image sur 2 
    if user_data.get_count() % 2 != 0:
        return Gst.PadProbeReturn.OK

    # Using the user_data to count the number of frames
    user_data.increment()
    string_to_print = f"Frame count: {user_data.get_count()}\n"

    # Get the caps from the pad
    format, width, height = get_caps_from_pad(pad)

    # If the user_data.use_frame is set to True, we can get the video frame from the buffer
    frame = None
    if user_data.use_frame and format is not None and width is not None and height is not None:
        # Get video frame
        frame = get_numpy_from_buffer(buffer, format, width, height)

    # Get the detections from the buffer
    roi = hailo.get_roi_from_buffer(buffer)
    detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

    # Parse the detections
    detection_count = 0
    detected = {
        "person1": False,
        "person2": False,
        "person3": False,
        "nico": False
    }

    for detection in detections:
        label = detection.get_label()
        if label in detected:
            detected[label] = True
            detection_count += 1

    if user_data.use_frame:
        # Note: using imshow will not work here, as the callback function is not running in the main thread
        # Let's print the detection count to the frame
        cv2.putText(frame, f"Detections: {detection_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Example of how to use the new_variable and new_function from the user_data
        cv2.putText(frame, f"{user_data.new_function()} {user_data.new_variable}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Convert the frame to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        user_data.set_frame(frame)

    # Compare the current detection state with the previous one and write log if there's a change
    timestamp =  datetime.now().astimezone().isoformat()#datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_needed = False  # Flag to check if log is needed

    with open(CSV_LOG_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)
        for person, state in detected.items():
            if state != user_data.previous_detection[person]:  # Check if the state has changed
                
                if person == "nico":
                    event_name = "nico=true" if state else "nico=false"
                    event = Event(event_name, timestamp)
                    send_event_signal(event)
                    print(f"[Signal envoye] --> {event_name} a {timestamp}")
                
                if not log_needed:  # Write a log only once if any state has changed
                    writer.writerow([
                        1,  # case_id (fixe pour l'instant)
                        timestamp,
                        "frame",
                        detected["person1"],
                        detected["person2"],
                        detected["person3"],
                        detected["nico"]
                    ])
                    log_needed = True  # Set flag to avoid multiple writes for the same frame

    # Update previous state for future comparisons
    user_data.previous_detection = detected.copy()

    return Gst.PadProbeReturn.OK

def start_detection(hef_path, label_path, input_src="rpi,framerate=30/1,width=640,height=360"):
    import sys
    sys.argv = [
        "detection.py",
        "--hef", hef_path,
        "--input", input_src,
        "--label", label_path
    ]
    user_data = user_app_callback_class()
    app = GStreamerDetectionApp(app_callback, user_data)
    app.run()


