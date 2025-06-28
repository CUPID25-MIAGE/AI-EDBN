import smtplib
from email.message import EmailMessage

# ------------- CONSTANTS ---------------

NAME = "Nicolas"
EMAIL = "livia.leroystone@gmail.com"

LIGHT_ON = "turned on the light"
LIGHT_OFF = "turned off the light"
SHUTTER_OPENED = "opened your shutter"
SHUTTER_CLOSED = "closed your shutter"

# --------------- CODE ------------------

def send_email(action):
    msg = EmailMessage()
    msg.set_content("Hello " + NAME + " :)\n I just " + action + ".\n See you later !\n CUPID")
    msg["Subject"] = "An action was taken in your absence"
    msg["From"] = "cupid25.P1@gmail.com"
    msg["To"] = EMAIL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("cupid25.P1@gmail.com", "wddo njtb oyjt tral")
        smtp.send_message(msg)

if __name__ == "__main__":
    send_email(SHUTTER_OPENED)