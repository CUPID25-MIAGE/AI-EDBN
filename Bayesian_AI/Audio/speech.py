import subprocess

def speak_text(text):
    piper_path = "/home/pi/Bayesian_AI/Piper/piper"
    model_path = "/home/pi/Bayesian_AI/Piper/fr_FR-siwis-medium.onnx"
    config_path = "/home/pi/Bayesian_AI/Piper/fr_FR-siwis-medium.onnx.json"
    output_path = "/home/pi/Bayesian_AI/Piper/speech.wav"

    command = [
        piper_path,
        "--model", model_path,
        "--config", config_path,
        "--output-file", output_path
    ]

    try:
        subprocess.run(command, input=text.encode('utf-8'), check=True)

        # Essaye d'abord sans forcer la carte son
        subprocess.run(["aplay", output_path], check=True)

    except subprocess.CalledProcessError as e:
        print(f"[Erreur Piper] : {e}")
