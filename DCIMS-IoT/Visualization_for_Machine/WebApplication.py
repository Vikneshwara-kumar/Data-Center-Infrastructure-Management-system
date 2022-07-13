# importing libraries

from flask import Flask, render_template, url_for, request, redirect, make_response
import paho.mqtt.client as mqtt
import ssl
import json
from time import time

sensor_data = {"temp": 0,
               "humid": 0,
               "motion": "off",
               "fire": "off",
               "fan": "off",
               "condition": "off",
               "servo": "off"
               }

app: Flask = Flask(__name__)


def on_connect(client, userdata, flags, rc):                                            # Function for establishing connection
    print("Connection returned result: " + str(rc))
    mqtt_subscriber.subscribe([('Area-1/Sensor_Data', 1), ('Area-1/Action', 1)])


def on_message(client, userdata, msg):                                                  # Function for receiving msgs
    a = msg.topic
    if a == "Area-1/Sensor_Data":                                                       #Topic:Area-1/Action to publish for sensor values
        t = json.loads(str(msg.payload.decode("utf-8")))
        sensor_data["temp"] = t["Temperature"]
        sensor_data["humid"] = t["Humidity"]
        sensor_data["motion"] = t["Motion"]
        sensor_data["fire"] = t["FireAlarm"]
        print(sensor_data)
    if a == "Area-1/Action":                                                            #Topic:Area-1/Action to publish for Actions values
        t = json.loads(str(msg.payload.decode("utf-8")))
        for key, value in t.items():
            if key == "Fan":
                sensor_data["fan"] = t["Fan"]
            if key == "Condition":
                sensor_data["condition"] = t["Condition"]
            if key == "Servo":
                sensor_data["servo"] = t["Servo"]



mqtt_subscriber = mqtt.Client()                                                             #mqtt subscriber object
mqtt_subscriber.on_connect = on_connect                                                     #assign on_connect function
mqtt_subscriber.on_message = on_message                                                     #assign on_message function
awshost = "a1xct602hf98vg-ats.iot.us-east-1.amazonaws.com"                                  #End-point.
awsport = 8883                                                                              #Port no.

caPath = "C:/Users/vikne/PycharmProjects/DCIMS-IoT/AWSIoT/Root-CA.pem"                      # Root_CA_Certificate_Name
certPath = "C:/Users/vikne/PycharmProjects/DCIMS-IoT/AWSIoT/certificate.pem.crt"            # <Thing_Name>.cert.pem
keyPath = "C:/Users/vikne/PycharmProjects/DCIMS-IoT/AWSIoT/private.pem.key"                 # <Thing_Name>.private.key

mqtt_subscriber.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)                                                                 # pass parameters
mqtt_subscriber.username_pw_set("username", "password")
mqtt_subscriber.connect(awshost, awsport, keepalive=60)                                     # connect to aws server
mqtt_subscriber.loop_start()

while 1 == 1:
    @app.route('/', methods=["GET", "POST"])
    def main():
        return render_template('base.html')


    @app.route('/data', methods=["GET", "POST"])
    def data():

        Temperature = int(sensor_data["temp"])
        Humidity = int(sensor_data["humid"])
        Motion = str(sensor_data["motion"])
        Fire_Alarm = str(sensor_data["fire"])
        Servo = str(sensor_data["servo"])
        Fan = str(sensor_data["fan"])
        Condition = str(sensor_data["condition"])

        data = [time() * 1000, Temperature, Humidity, Motion, Fan, Fire_Alarm, Servo, Condition]

        response = make_response(json.dumps(data))

        response.content_type = 'application/json'

        return response


    if __name__ == "__main__":
        app.run(debug=True)