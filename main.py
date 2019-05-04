#Programme à lancer pour une reconnaissance facial par la caméra de la Rapsberry Pi et envoie d'un mail avec une image

import cv2
import sys
from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading

email_update_interval = 10 #Interval de temps d'envoie d'un mail
video_camera = VideoCamera(flip=True) #Crée un objet caméra, retournez verticalement
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml") #OpenCV Classifier (reconnaissance facial)

#App Global à ne pas éditer
app = Flask(__name__) #Appelle la dernière fonction pour lancer le serveur
app.config['BASIC_AUTH_USERNAME'] = 'admin' #Username pour accéder au site
app.config['BASIC_AUTH_PASSWORD'] = 'admin' #MDP pour accéder au site
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0 #Initialisation du dernier temps de reconnaissance facial

def check_for_objects(): #Fonction de détection d'objet
	global last_epoch
	while True:
		try:
			frame, found_obj = video_camera.get_object(object_classifier) #appelation la fonction de videm_camera.get_object qui est dans le fichier camera.py
			if found_obj and (time.time() - last_epoch) > email_update_interval: #Test si objet trouvé et si le temps actuel - temps de la dernière > interval mail
				last_epoch = time.time() #Changement de la valeur last_epoch par le temps du dernier mouvement
				print ("Envoie mail") #Affichage du texte dans le terminal
				sendEmail(frame) #Utilisation de la fonction sendEmail du fichier mail.py avec récupération de frame et du found_obj pour intégration dans le mail
				print ("Fait") #Affichage du texte dans le terminal
		except:
			print ("PB envoie mail", sys.exc_info()[0]) #Affiche des erreurs dans le terminal lors du non envoie du mail

@app.route('/')
@basic_auth.required
def index(): #Fonction pour le template du site serveur
    return render_template('index.html')

def gen(camera): #Fonction de récupération des images par la caméra
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
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
