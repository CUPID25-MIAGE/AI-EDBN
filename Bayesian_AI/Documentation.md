Documentation d’installation et d’utilisation du projet Bayesian-AI avec Vosk et Hailo sur Raspberry Pi
Présentation
Ce projet permet d’utiliser un modèle de reconnaissance vocale Vosk, couplé à un pipeline d’inférence vidéo optimisé pour un module Hailo sur Raspberry Pi 5.
Le but est d’avoir un système de reconnaissance vocale + traitement vidéo avec communication entre processus via Flask et signaux.

Prérequis
Matériel :

Raspberry Pi 5

Caméra compatible (ex. IMX708)

Module d’accélération Hailo8

Système :

Raspberry Pi OS (version récente, 64 bits recommandée)

Python 3.11+

Librairies systèmes (GStreamer, libcamera, etc.)

Logiciels nécessaires :

Vosk API (modèle vocal français petit)

Environnement Python virtuel avec dépendances (Flask, pyaudio, hailo-sdk...)

Outils Hailo (tappas-core, libs, drivers)

Étapes d’installation et configuration
1. Préparer le Raspberry Pi
Mettre à jour le système

bash
Copier
Modifier
sudo apt update && sudo apt upgrade -y
Installer les dépendances système nécessaires (GStreamer, libcamera, pilotes)

bash
Copier
Modifier
sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev python3-pip python3-venv -y
Configurer la caméra (si ce n’est pas déjà fait)

bash
Copier
Modifier
sudo raspi-config
# Activer l’interface caméra et redémarrer
2. Cloner le dépôt du projet
bash
Copier
Modifier
cd /home/pi
git clone <url-du-depot-Bayesian-AI.git>
cd Bayesian-AI
3. Configurer l’environnement Python
Activer l’environnement virtuel spécifique à Hailo

bash
Copier
Modifier
source Video/hailo_rpi5_examples/setup_env.sh
Ce script :

Vérifie et active le virtualenv venv_hailo_rpi5_examples

Configure les variables d’environnement nécessaires pour Hailo et tappas-core

4. Préparer le modèle Vosk
Vérifier que le modèle Vosk français est bien placé dans /home/pi/Bayesian-AI/vosk-model-small-fr-0.22/

Le modèle doit contenir les fichiers d’index, graph, iVector, etc. (fourni avec le dépôt ou téléchargé)

5. Lancer l’application
bash
Copier
Modifier
python mainTest2.py
Le script lance :

Le service Flask pour la communication REST

Le pipeline vidéo GStreamer configuré avec les plugins Hailo

La reconnaissance vocale Vosk

La capture caméra et traitement Hailo

6. Utilisation
Le système affiche un message Micro prêt. Dites 'cupide'...

Parlez la commande déclencheuse (ex: “cupide explique”)

Le système répond, active des événements, et traite les signaux internes

Pour arrêter proprement, utilisez CTRL+C dans le terminal

Dépannage
Pas d’activation du virtualenv ?
Vérifiez le script setup_env.sh, qu’il pointe bien vers le bon environnement et que Python 3.11 est utilisé.

Problèmes caméra ?
Vérifiez la configuration avec libcamera-hello
Assurez-vous que la caméra est détectée via /dev/media* et /dev/video*

Le modèle Vosk ne se charge pas ?
Vérifiez que le chemin vers le modèle est correct dans mainTest2.py
Assurez-vous que tous les fichiers requis sont présents.

Arrêt via CTRL+C ne fonctionne pas ?
Implémentez un handler dans Python pour capturer KeyboardInterrupt et fermer proprement la boucle.

Fichiers et répertoires importants
/home/pi/Bayesian-AI/mainTest2.py : script principal

/home/pi/Bayesian-AI/Video/hailo_rpi5_examples/setup_env.sh : script d’activation environnement

/home/pi/Bayesian-AI/vosk-model-small-fr-0.22/ : modèle Vosk français

/home/pi/Bayesian-AI/Video/yolo/ : fichiers HEF et JSON pour Hailo (modèles d’inférence)

/home/pi/Bayesian-AI/Piper/ : gestion synthèse vocale (piper)

Conseils avancés
Pour un déploiement en production, utiliser un serveur WSGI (gunicorn, uwsgi) pour Flask

Surveiller les logs avec journalctl ou redirection vers fichier

Automatiser le lancement au démarrage avec systemd ou crontab

Optimiser les paramètres GStreamer et Hailo pour le hardware
