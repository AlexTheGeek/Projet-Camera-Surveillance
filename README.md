# Projet-Camera-Surveillance-Exterieure

Dans ce projet nous utilisons une Raspberry Pi 3B+. 
La caméra de surveilance fonctionne avec OpenCV4 pour la détection de mouvement. La caméra enverra un mail contenant une image du mouvement. La caméra possède aussi un serveur pour voir une vidéo en direct.

## Configuration de la Raspberry
Dans ce projet, nous utilisons une Quimat Raspberry Pi Camera IR. Avant il faut activer sur la Raspberry 
Ouvrez le terminal et exécutez :
````
sudo raspi-config
`````
Sélectionnez `Interface Options` puis `Camera` et activez-la et cliquez sur `Finish`.

Pour vérifier que la caméra marche entrez :
`````
sudo raspistill -o image.png
``````

## Installation de OpenCV4
Pour installer OpenCV4, nous avons utilisez le [tutroriel](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/).
