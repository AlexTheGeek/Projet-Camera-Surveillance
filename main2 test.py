import cv2
import sys
from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading
import RPi.GPIO as GPIO
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

email_update_interval = 10
video_camera = VideoCamera(flip=True) 
object_classifier = cv2.CascadeClassifier("models/fullbody_recognition_model.xml")


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
    print('Mouvement detecte  a :')
    date = datetime.datetime.now()
    print(date.strftime("%d-%m-%Y %H:%M:%S"))
    msg = MIMEMultipart()
    msg['From'] = 'projetcamera2019@gmail.com'
    msg['To'] = 'albrunet2000@gmail.com'
    msg['Subject'] = 'Le sujet de mon mail'
    message = 'Bonjour !'
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login('projetcamera2019@gmail.com', 'A6M8O4R5')
    mailserver.sendmail('projetcamera2019@gmail.com','albrunet2000@gmail.com', msg.as_string())
    mailserver.quit()


try:
    GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=my_callback)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print("Finish...")
GPIO.cleanup()


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
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
