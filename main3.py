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

email_update_interval = 10
video_camera = VideoCamera(flip=True)
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml")


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0

SENSOR_PIN = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def my_callback(channel):
    frame, found_obj = video_camera.get_object(object_classifier)
    global last_epoch
    date = datetime.datetime.now()
    d = date.strftime("%S")
    print(d)
    if d != "01" and (time.time() -  last_epoch) > email_update_interval and found_obj:
      last_epoch = time.time()
      print("Detection de mouvement")
      sendEmail(frame)
    else:
      print("Rien")

try:
    GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=my_callback)
except:
	print("Rien")


@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    t = threading.Thread(target=(), args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
