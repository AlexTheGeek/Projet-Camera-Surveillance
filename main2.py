#Programme à lancer pour une détection de mouvement et envoie d'un mail simple (sans images)

import cv2
import sys
from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading
import RPi.GPIO as GPIO
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

email_update_interval = 10 #Interval de temps d'envoie d'un mail
video_camera = VideoCamera(flip=True) #Crée un objet caméra, retournez verticalement
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml") #OpenCV Classifier (reconnaissance facial)

#App Global à ne pas éditer
app = Flask(__name__) #Appelle la dernière "fonction" pour lancer le serveur
app.config['BASIC_AUTH_USERNAME'] = 'admin' #Username pour accéder au site
app.config['BASIC_AUTH_PASSWORD'] = 'admin' #MDP pour accéder au site
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0 #Initialisation du dernier temps de détection de mouvement

SENSOR_PIN = 7 #Numéro du Pin du GPIO de la Raspberry Pi pour le HC-SR501

GPIO.setmode(GPIO.BCM) #Spécification du mode que l'on utilise (ici : BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN) #Configuration de la channel 7 en Input


def my_callback(channel): #Fonction appelé dès lors détection d'un mouvement
    global last_epoch
    date = datetime.datetime.now() #Récupération de la date et l'heure actuel (pour les tests et vérifications)
    d = date.strftime("%S") #Variable de récupération des secondes (str) (pour les tests et vérifications)
    print(d) #Affiche pour vérifier
    if d != "01" and (time.time() - last_epoch) > email_update_interval: #Test si la valeur des secondes est différentes de 01 (sinon répétition d'un mouvement toutes les minutes à 01s) et test si le temps - à la dernière détection de mouvement > interval d'envoie de mail
      last_epoch = time.time() #Changement de la valeur last_epoch par le temps du dernier mouvement
      print('Mouvement detecte  a :') #Affichage du texte dans le terminal
      date = datetime.datetime.now() #Récupération de la date et l'heure actuel
      print(date.strftime("%d-%m-%Y %H:%M:%S")) #Affichage du texte dans le terminal
      msg = MIMEMultipart() #Initialisation d'un message à plusieurs partie sur serveur Google
      msg['From'] = 'adressemaile@gmail.com' #Adresse mail de l'expéditeur
      msg['To'] = 'adressemaild@gmail.com' #Adresse mail du destinataire
      msg['Subject'] = 'Alerte de securite' #Objet du mail
      message = 'Mouvement detecte' #Corps du mail
      msg.attach(MIMEText(message)) #Récupération du message
      mailserver = smtplib.SMTP('smtp.gmail.com', 587) #Connection au serveur Google
      mailserver.ehlo()
      mailserver.starttls()
      mailserver.ehlo()
      mailserver.login('adressemaile@gmail.com', 'mdp') #Connection avec les informations de connection au serveur Google
      mailserver.sendmail('adressemaile@gmail.com','adressemaild@gmail.com', msg.as_string()) #Ligne d'envoie du mail
      mailserver.quit() #Déconnexion du serveur Google


try:
    GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=my_callback) #Essaye de détecter un événement (mouvement) sur le pin, s'il y a une impultion électrique alors appelle la fonction my_callback
except:
	print("Rien")


@app.route('/')
@basic_auth.required
def index(): #Fonction pour le template du site serveur
    return render_template('index.html')

def gen(camera): #Fonction de récupération des images par la caméras
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed(): #Fonction pour le live sur le site local
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#App Glocal pour le serveur
if __name__ == '__main__':
    t = threading.Thread()
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
