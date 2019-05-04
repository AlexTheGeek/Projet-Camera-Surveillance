# Projet Caméra Surveillance

Dans ce projet nous utilisons une Raspberry Pi 3B+. 
La caméra de surveilance fonctionne avec OpenCV4 pour la détection de mouvement. La caméra enverra un mail contenant une image du mouvement d'objet. En complément, un détecteur de mouvement IR permet de détecter de mouvement de personne. La caméra possède aussi un serveur pour voir une vidéo en direct.

## Préparation de la Raspberry
### Connexion de la Camera


### Connexion du PIR HC-SR501


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
Nous avons besoin d'OpenCV4 (Python 3) pour la détection de mouvement d'objet.

#### Installation des dépendance d'OpenCV4
Commencez par faire les mises à jour de la Raspberry Pi :
``````
sudo apt-get update && sudo apt-get upgrade
``````

Installons les outils de développement (CMake) :
```````
sudo apt-get install build-essential cmake unzip pkg-config
```````

Installons des bibliothèques d'images et de vidéos :
````````
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
`````````

Installons une interface graphique utilisateur backend (GTK) :
```````
sudo apt-get install libgtk-3-dev
````````

Installons un paquet pour GTK :
````````
sudo apt-get install libcanberra-gtk*
````````

Installons deux paquets qui contiennent des optimisations numérique pour OpenCV4 :
``````
sudo apt-get install libatlas-base-dev gfortran
``````

Installation Python 3 :
```````
sudo apt-get install python3-dev
````````

#### Téléchargement d'OpenCV4 pour Rapsberry Pi
Naviguez jusqu'au dossier `Home` de votre Raspberry Pi.
```````
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip
unzip opencv.zip
unzip opencv_contrib.zip
```````

Renommons les répertoires:
````````
mv opencv-4.0.0 opencv
mv opencv_contrib-4.0.0 opencv_contrib
`````````

#### Configuration de l'environnement virtuel de Python 3 pour OpenCV4
Installons un Python Paquet Manager, pip :
``````
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
```````

Installons virtualenv et virtualenvwrapper pour un environnment virtuel Python :
```````
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/get-pip.py ~/.cache/pip
````````




Installons le paquet Python prérequis pour OpenCV, NumPy :
``````
pip install numpy
``````

#### CMake et compilation d'OpenCV4



#### Relions OpenCV 4 à votre environnement virtuel Python 3
Créons un lien symbolique depuis l'installation d'OpenCV dans le répertoire system site-packages vers notre environnement virtuel :
```````
cd ~/.virtualenvs/cv/lib/python3.5/site-packages/
ln -s /usr/local/python/cv2/python-3.5/cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so
````````

#### Lancement d'OpenCV4
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
fromEmail = 'adressemaile@gmail.com' #Entrez une adresse mail Google d'envoie du mail
fromEmailPassword = 'mdp' #Entrez le mot de passe du compte Google (Pas de double authentification)
toEmail = 'adressemaild@gmail.com' #Entrez une adresse mail de réception
``````

## Lancement du programme
Lancez le programme avec la commande :
``````
python main.py
``````
Vous pouvez choisir quel type de reconnaissance vous souhaitez :  
* `main.py` : reconnaissance avec la caméra (OpenCV) et envoie d'un mail avec prise d'une photo du mouvement
* `main2.py` : reconnaissance avec le PIR et envoie d'un mail avec texte
* `main2.1.py` : reconnaissance avec le PIr et envoie d'un mail et prise d'un photo du mouvement

On peut voir le flux vidéo en direct en allant sur `http://<ip_raspberry>:5000` dans un navigateur internet sur le réseau local. Pour visioner depuis l'extérieur, vous pouvez  ouvrir un port de votre box pour la raspberry : `http://<ip_box>:<port_ouvert>`(Méthode non sécurisée).



