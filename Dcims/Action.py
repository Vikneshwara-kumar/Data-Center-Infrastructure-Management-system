import paho.mqtt.client as mqtt
import os
import socket
import ssl
import json
from time import sleep
import RPi.GPIO as GPIO



GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
pwm = GPIO.PWM(17, 50)
pwm.start(0)
emp_count = set()


def SetAngle(angle):
    duty = (angle / 18) + 2
    GPIO.output(17, True)
    pwm.ChangeDutyCycle(duty)


def fan(speed):
    print("Fan :" + str(speed))

    if (str(speed) == 'off'):
        GPIO.output(23, GPIO.LOW)
        GPIO.output(14, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)
    if (str(speed) == 'low'):
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(14, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)
    if (str(speed) == 'medium'):
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(14, GPIO.HIGH)
        GPIO.output(15, GPIO.LOW)
    if (str(speed) == 'high'):
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(14, GPIO.HIGH)
        GPIO.output(15, GPIO.HIGH)


def servo(state):
    print("Servo :" + str(state))
    if (str(state) == 'off'):
        SetAngle(0)

    if (str(state) == 'on'):
        SetAngle(180)


def buzzer(type):
    print("Buzzer :" + str(type))
    if (str(type) == 'off'):
        GPIO.output(27, GPIO.LOW)

    if (str(type) == 'on'):
        GPIO.output(27, GPIO.HIGH)
        sleep(2)
        GPIO.output(27, GPIO.LOW)


def on_connect(client, userdata, flags, rc):  # func for making connection
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Area-1/Action", 1)  # Subscribe to "Actions" topic


def on_message(client, userdata, msg):  # Func for receiving msgs
    act = json.loads(str(msg.payload.decode("utf-8")))
    for key, value in act.items():
        if key == "Fan_A":
            fan(value)
        if key == "Servo_A":
            servo(value)
        if key == "Buzzer_A":
            buzzer(value)

mqtt_subscriber = mqtt.Client()
mqtt_subscriber.on_connect = on_connect
mqtt_subscriber.on_message = on_message
awshost = "a1xct602hf98vg-ats.iot.us-east-1.amazonaws.com"
awsport = 8883

caPath = "C:/Users/vikne/PycharmProjects/DCIMS-IoT/AWSIoT/Root-CA.pem"  # Root_CA_Certificate_Name
certPath = "C:/Users/vikne/PycharmProjects/DCIMS-IoT/AWSIoT/certificate.pem.crt"  # <Thing_Name>.cert.pem
keyPath = "C:/Users/vikne/PycharmProjects/DCIMS-IoT/AWSIoT/private.pem.key"  # <Thing_Name>.private.key

mqtt_subscriber.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)  # pass parameters
mqtt_subscriber.username_pw_set("username", "password")
mqtt_subscriber.connect(awshost, awsport, keepalive=60)  # connect to aws server

while True:
    mqtt_subscriber.loop_start()