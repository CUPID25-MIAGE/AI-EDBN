import signal
import sys

def signal_handler(sig, frame):
    print("\nArret demande via CTRL+C, fermeture en cours...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
