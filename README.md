# Projet Caméra Surveillance Extérieure

Dans ce projet nous utilisons une Raspberry Pi 3B+. 
La caméra de surveilance fonctionne avec OpenCV4 pour la détection de mouvement. La caméra enverra un mail contenant une image du mouvement d'objet. En complément, un détecteur de mouvement IR permet de détecter de mouvement de personne. La caméra possède aussi un serveur pour voir une vidéo en direct.

## Configuration de la Raspberry
Dans ce projet, nous utilisons une Quimat Raspberry Pi Camera IR. Avant il faut activer la camera sur la Raspberry.

Ouvrez le terminal et exécutez :
````
sudo raspi-config
`````
Sélectionnez `Interface Options` puis `Camera` et activez-la et cliquez sur `Finish`.

Pour vérifier que la caméra marche entrez :
`````
sudo raspistill -o image.png
``````
## Installation des dépendances
### Installation OpenCV4
Nous avons besoin d'OpenCV4 pour la détection de mouvement d'objet. Pour installer OpenCV4 (Python 3), nous avons utilisez le [tutroriel](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/).
OpenCV fonctionne sur un environnement virtuel. Pour y accéder utiliser les commandes suivantes :
``````
source ~/.profile
workon cv
```````

### Installaiton Flask

`````
pip install flask
`````

### Installation Picamera

`````
pip install picamera
`````

### Installation Imutils

`````
pip install imutils
`````

### Installation Flask-BasicAuth

`````
pip install Flask-BasicAuth
``````

## Personnalisation du programme
Vous pouvez mofier la partie main en modifiant l'authentification au serveur de la raspberry pi :
`````
app.config['BASIC_AUTH_USERNAME'] = 'admin' #Changez l'utilisateur
app.config['BASIC_AUTH_PASSWORD'] = 'admin' #Changez le mot de passe
app.config['BASIC_AUTH_FORCE'] = True
`````

Dans le main, la modification de paramètres :
``````
email_update_interval = 10 #N'envoie un courriel qu'une seule fois dans cet intervalle de temps
video_camera = VideoCamera(flip=True) #Crée un objet caméra, retournez verticalement
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml") #OpenCV classifier
``````
Vous pouvez aussi utiliser d'autre object de détection en changant `"models/facial_recognition_model.xml"` dans `object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml")` par les autres objets de détection qui sont dans le dossier `models`.

Modifiez aussi les informations du mail :
``````
fromEmail = 'addressemaile@gmail.com' #Entrez une addresse mail Google d'envoie du mail
fromEmailPassword = 'mdp' #Entrez le mot de passe du compte Google (Pas de double authentification)
toEmail = 'addressemailr@gmail.com' #Entrez une addresse mail de réception
``````

## Lancement du programme

Lancez le programme avec la commande :
``````
python main.py
``````
On peut voir le flux vidéo en direct en allant sur `http://<ip_raspberry>:5000` dans un navigateur internet sur le réseau local. Pour visioner depuis l'extérieur, vous pouvez  ouvrir un port de votre box pour la raspberry : `http://<ip_box>:<port_ouvert>`.



