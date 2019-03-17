import RPi.GPIO as GPIO
import time
 
SENSOR_PIN = 23
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)
 
def my_callback(channel):
    print('Mouvement detecte !')

try:
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=my_callback)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print "Finish..."
GPIO.cleanup()
