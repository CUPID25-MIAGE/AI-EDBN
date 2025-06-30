import subprocess

music_process = None  # Global pour garder le processus actif

def launch_music(audio_path="/home/pi/Bayesian-AI/Audio/rap.mp3"):
    global music_process

    if music_process and music_process.poll() is None:
        print("Musique dÃ©jÃ  en cours.")
        return
    try:
        print("Lancement de la musique...")
        music_process = subprocess.Popen(["mpg123", audio_path])
    except Exception as e:
        print(f"[Erreur musique] : {e}")

def stop_music():
    global music_process

    if music_process and music_process.poll() is None:
        print("Arret de la musique...")
        music_process.terminate()
    else:
        print("Aucune musique en cours.")
