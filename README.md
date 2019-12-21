# Projet Caméra Surveillance

## Sommaire
1. [Présentation du projet](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#pr%C3%A9sentation-du-projet)
2. [Présentation du matériel](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#pr%C3%A9sentation-du-mat%C3%A9riel)
3. [Présentation de la Raspberry Pi](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#pr%C3%A9paration-de-la-raspberry)
    * [Connexion dela caméra](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#connexion-de-la-camera)
    * [Connexion du PIR-HCSR501](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#connexion-du-pir-hc-sr501)
4. [Configuration de la Raspberry Pi](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#configuration-de-la-raspberry)
5. [Installation des dépendances](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#installation-des-d%C3%A9pendances)
    * [Installation d'OpenCV4](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#installation-opencv4)
    * [Installation de Flask](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#installaiton-flask)
    * [Installation de Picamera](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#installation-picamera)
    * [Installation Imutils](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#installation-imutils)
    * [Installation de Flask-BasicAuth](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#installation-flask-basicauth)
6. [Personnalisation du programme](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#personnalisation-du-programme)
7. [Lancement du programme](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#lancement-du-programme)
8. [Réalisations supplémentaires](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#r%C3%A9alisations-suppl%C3%A9mentaires)
    * [Réalisation de l'application](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#r%C3%A9alisation-de-lapplication)
    * [Réalisation du support pour la caméra et le PIR](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#r%C3%A9alisation-du-support-pour-la-cam%C3%A9ra-et-du-pir)
9. [Documents supplémentaires](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#documentation)
10. [Crédit](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#cr%C3%A9dit)
11. [Possibilités supplémentaires](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#cr%C3%A9dit)
12. [Liens](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#liens)
13. [Contact](https://github.com/AlexTheGeek/Projet-Camera-Surveillance#contact)


## Présentation du projet
Dans ce projet nous utilisons une Raspberry Pi 3B+.
La caméra de surveillance fonctionne avec OpenCV4 pour la détection de mouvement. La caméra enverra un mail contenant une image prise lors d'un mouvement. En complément, un détecteur de mouvement IR permet de détecter le mouvement d'une personne. La caméra possède aussi un serveur pour voir une vidéo en direct.

## Présentation du matériel
La Raspberry Pi 3 B+ possède le Wifi 2,4GHz et 5GHz faciitant la connexion de la Raspberry à internet. La Raspberry possède un port éthernet qui permet d'avoir un débit internet plus fiable pour la Raspberry Pi. Vous pouvez vous référez à la documentation officielle de la Raspberry Pi : [présentation](https://static.raspberrypi.org/files/product-briefs/Raspberry-Pi-Model-Bplus-Product-Brief.pdf).  
Nous utilisons aussi le PIR HC-SR501 qui possède une détection de mouvement par infra-rouge.


## Préparation de la Raspberry
### Connexion de la Caméra
![CAM1](https://alexthegeek.github.io/Projet-Camera-Surveillance/Images/CAM1.jpg)
Pour connecter la caméra, il faut brancher chaque broche du cable de la caméra dans le port Camera de la Raspberry Pi.
![CAM2](https://alexthegeek.github.io/Projet-Camera-Surveillance/Images/CAM2.jpg)

### Connexion du PIR HC-SR501
![PIR1](https://alexthegeek.github.io/Projet-Camera-Surveillance/Images/PIR1.jpg)
Dans ce projet, nous utiliserons les pins 2 - 6 - 26 mais vous pouvez utiliser d'autres ports en suivant la [documentation de la Raspberry](https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf).  
Identifiez chaque port du PIR en soulevant le "petit chapeau" :
![PIR2](https://alexthegeek.github.io/Projet-Camera-Surveillance/Images/PIR2.jpg)

Tout à d'abord connectez le pin VCC du PIR sur le pin 2 (VCC 5V) de la Raspberry Pi.  
Après connectez GRND du PIR sur le pin 6 (GRND) de la Raspberry Pi.  
Pour finir sur le dernier port du PIR (OUT) sur le pin 26 (GPIO 7) de la Raspberry Pi.  
![PIR3](https://alexthegeek.github.io/Projet-Camera-Surveillance/Images/PIR3.jpg)  


## Configuration de la Raspberry
Dans ce projet, nous utilisons une Quimat Raspberry Pi Camera IR. Avant il faut activer la caméra sur la Raspberry.

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

#### Installation des dépendances d'OpenCV4
Commencez par faire les mises à jour de la Raspberry Pi :
``````
sudo apt-get update && sudo apt-get upgrade
``````

Installez les outils de développement (CMake) :
```````
sudo apt-get install build-essential cmake unzip pkg-config
```````

Installez des bibliothèques d'images et de vidéos :
````````
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
`````````

Installez une interface graphique utilisateur backend (GTK) :
```````
sudo apt-get install libgtk-3-dev
````````

Installez un paquet pour GTK :
````````
sudo apt-get install libcanberra-gtk*
````````

Installez deux paquets qui contiennent des optimisations numériques pour OpenCV4 :
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

Renommez les répertoires :
````````
mv opencv-4.0.0 opencv
mv opencv_contrib-4.0.0 opencv_contrib
`````````

#### Configuration de l'environnement virtuel de Python 3 pour OpenCV4
Installez un Python Paquet Manager, pip :
``````
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
```````

Installez `virtualenv` et `virtualenvwrapper` pour un environnement virtuel Python :
```````
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/get-pip.py ~/.cache/pip
````````

Modifiez `~/.profile` :
``````
echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile
```````
Vous pouvez aussi le modifier avec vim ou nano (un éditeur de texte du terminal).  

``````
source ~/.profile
``````

Créez l'environnement virtuel OpenCV4 + Python 3:
```````
mkvirtualenv cv -p python3
````````

Vérifiez que vous êtes bien dans l'environnement `cv`
``````
workon cv
``````

Installez le paquet Python prérequis pour OpenCV, NumPy :
``````
pip install numpy
``````

#### CMake et compilation d'OpenCV4
``````
cd ~/opencv
mkdir build
cd build
```````

Exécution CMake pour OpenCV4 :
````````
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
      -D ENABLE_NEON=ON \
      -D ENABLE_VFPV3=ON \
      -D BUILD_TESTS=OFF \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D BUILD_EXAMPLES=OFF ..
``````````  

Vérifiez que dans le terminal vous avez `Non-free algorithms: YES`.  
Dans `Python 3`:  
`Interpreter: .../.virtualenvs/cv/...`  
`numpy: .../.virtualenvs/cv/...`  

Compilation d'OpenCV4 :  
````
make -j4
`````
Si des erreurs apparaissent vous pouvez seulement faire `make`.  

Installation d'OpenCV4
`````
sudo make install
sudo ldconfig
```````


#### Relions OpenCV 4 à votre environnement virtuel Python 3
Créez un lien symbolique depuis l'installation d'OpenCV dans le répertoire system site-packages vers votre environnement virtuel :
```````
cd ~/.virtualenvs/cv/lib/python3.5/site-packages/
ln -s /usr/local/python/cv2/python-3.5/cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so
````````

#### Lancement d'OpenCV4
OpenCV fonctionne sur un environnement virtuel. Pour y accéder utilisez les commandes suivantes :
``````
source ~/.profile
workon cv
```````

### Installation Flask
Fask est un microframework pour des applications web Python, pour le routage d'URL de site.
`````
pip install flask
`````

### Installation PiCamera
PiCamera est un paquet qui permet d'avoir une interface pour le module caméra Raspberry Pi pour Python 3.
`````
pip install picamera
`````

### Installation Imutils
Imutils est une série de fonctions de traitement d'image plus simple pour OpenCV4 et Python 3.
`````
pip install imutils
`````

### Installation Flask-BasicAuth
Flask-BasicAuth est une extension Flask qui permet de protéger une page web grâce à une authentification par accès de base HTTP.
`````
pip install Flask-BasicAuth
``````

## Personnalisation du programme
Vous pouvez modifier la partie `main` en modifiant l'authentification au serveur de la raspberry pi :
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
Vous pouvez aussi utiliser d'autres objets de détection en changeant `"models/facial_recognition_model.xml"` dans `object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml")` par les autres objets de détection qui sont dans le dossier `models`.

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
* `main.py` : reconnaissance avec la caméra (OpenCV) et envoi d'un mail avec prise d'une photo du mouvement
* `main2.py` : reconnaissance avec le PIR et envoi d'un mail avec texte
* `main2.1.py` : reconnaissance avec le PIR et envoi d'un mail et prise d'une photo du mouvement
* `main3.py`: reconnaissance avec le PIR et la caméra (facial) et envoi d'un mail et prise d'une photo du mouvement

On peut voir le flux vidéo en direct en allant sur `http://<ip_raspberry>:5000` dans un navigateur internet sur le réseau local.  
Pour visionner depuis l'extérieur, vous pouvez  ouvrir un port de votre box pour la Raspberry : `http://<ip_box>:<port_ouvert>`(Méthode non sécurisée).  
De plus, pour un fonctionnement optimal, vous pouvez utiliser une ip statique pour la Raspberry pour éviter de rechercher l'ip à chaque fois.  
Pour connaître l'adresse ip de la Raspberry Pi vous pouvez taper dans le terminal : `hostname -I`.  


## Réalisations supplémentaires
### Réalisation de l'application
Début de l'application un prototype de l'application faite sur Adobe XD.  
[Prototype (Adobe XD)](https://alexthegeek.github.io/Projet-Camera-Surveillance/Application/Prototype_Cam.xd)  
[Prototype (zip --> png)](https://alexthegeek.github.io/Projet-Camera-Surveillance/Application/Prototype_App.zip)  
[Prototype (zip --> png(iPhone - iPad - Android (Mobile et Tablette))](https://alexthegeek.github.io/Projet-Camera-Surveillance/Application/Prototype_App_V2.zip)  
[Prototype Final](https://alexthegeek.github.io/Projet-Camera-Surveillance/Application/Prototype_App_V3.zip)  
Développement de l'application avec [Ionic](https://ionicframework.com/)  



### Réalisation du support pour la caméra et du PIR
Réalisation du prototype de support sur SolidWorks puis son impression 3D grâce à l'imprimante 3D Ultimaker.  
[Plan de la carte Raspberry Pi 3B+](https://www.raspberrypi.org/documentation/hardware/raspberrypi/mechanical/rpi_MECH_3bplus.pdf)    
[Plan de la boite Raspberry Pi 3B+](https://www.raspberrypi.org/documentation/hardware/raspberrypi/mechanical/rpi_MECH_3bplus_case.pdf)  
[Fichier SolidWorks du support (zip)](https://drive.google.com/file/d/10cG60MQHcWESOI00FiV3FxtPIc2hNC-3/view?usp=sharing) 


## Documents supplémentaires
[Manuel d'utilisation](https://alexthegeek.github.io/Projet-Camera-Surveillance/Documents/manuel.pdf)   
[Cahier des charges](https://alexthegeek.github.io/Projet-Camera-Surveillance/Documents/Cahier_des_charges.pdf)  
[Planning](https://alexthegeek.github.io/Projet-Camera-Surveillance/Documents/Planning.pdf)  
[Compte Rendu](https://alexthegeek.github.io/Projet-Camera-Surveillance/Documents/Compte_Rendu.pdf)  

## Possibilités supplémentaires
Nous avons aussi la possibilité d'envoyer une notification push sur votre téléphone (iOS ou Android) en utilisant IFTTT.  
Intégrez l'API de IFTTT dans votre code Python (vous pouvez la trouver en recherchant Webhooks dans IFTTT).  
Par la suite, vous devez créer une Applet de la manière suivant : If `Webhooks` then `Notifications`.  


## Crédit
Projet de première année STPI à l'INSA Centre Val de Loire.  
Membre de l'équipe :
* Alexis Brunet
* Matthieu Maindroux
* Omar Hadhar
* Roman Magnier

## Liens
[Chaine Youtube](https://www.youtube.com/channel/UCkh9bHsU9Y0lxfIJOGlvY6A?view_as=subscriber)  
[Site Web](https://alexthegeek.github.io/Projet-Camera-Surveillance/)

## Contact
Mail : [projetcamera2019@gmail.com](mailto:projetcamera2019@gmail.com)
