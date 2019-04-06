import RPi.GPIO as GPIO
import time
import datetime

SENSOR_PIN = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def my_callback(channel):
    print('Mouvement detecte  a :')
    date = datetime.datetime.now()
    print(date.strftime("%d-%m-%Y %H:%M:%S"))
try:
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=my_callback)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print ("Finish...")
GPIO.cleanup()
