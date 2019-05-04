import RPi.GPIO as GPIO
import time
import datetime

SENSOR_PIN = 7 #Numéro du Pin du GPIO de la Raspberry Pi pour le HC-SR501

GPIO.setmode(GPIO.BCM) #Spécification du mode que l'on utilise (ici : BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN) #Configuration de la channel 7 en Input

def my_callback(channel): #Fonction appelé dès lors détection d'un mouvement
    print('Mouvement detecte  a :') #Affichage dans le terminal
    date = datetime.datetime.now() #Récupération de la date et de l'heure actuelle
    print(date.strftime("%d-%m-%Y %H:%M:%S")) #Affichage de la date et l'heure du mouvement
try:
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=my_callback) #Essaye de détecter un événement (mouvement) sur le pin, s'il y a une impultion électrique alors on appelle la fonction my_callback
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print ("Finish...") #Affiche dès lors du "crt+C"
GPIO.cleanup()
