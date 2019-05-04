#Programme à lancer pour une détection de mouvement et envoie d'un mail avec une image

import cv2
import sys
from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading
import RPi.GPIO as GPIO
import datetime

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
    frame, found_obj = video_camera.get_object(object_classifier)
    global last_epoch
    date = datetime.datetime.now() #Récupération de la date et l'heure actuel (pour les testes et vérifications)
    d = date.strftime("%S") #Variable de récupération des secondes (str) (pour les testes et vérifications)
    print(d) #Affiche pour vérifier
    if d != "01" and (time.time() -  last_epoch) > email_update_interval : #Teste si la valeur des secondes est différentes de 01 (sinon répétition d'un mouvement toutes les minutes à 01s) et test si le temps - à la dernière détection de mouvement > interval d'envoie de mail
      last_epoch = time.time() #Changement de la valeur last_epoch par le temps du dernier mouvement
      print('Mouvement detecte  a :') #Affichage du texte dans le terminal
      date = datetime.datetime.now() #Récupération de la date et l'heure actuel
      print(date.strftime("%d-%m-%Y %H:%M:%S")) #Affichage du texte dans le terminal
      print("Envoie mail") #Affichage du texte dans le terminal
      sendEmail(frame) #Utilisation de la fonction sendEmail du fichier mail.py avec récupération de frame pour intégration dans le mail
      print("Fait") #Affichage du texte dans le terminal
    else:
      print("Rien") #Si mouvement détecter dans l'interval d'envoie de mail et si les secondes sont égales à 01 alors on affiche "Rien" dans le else pour vérification

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
    t = threading.Thread(target=(), args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
