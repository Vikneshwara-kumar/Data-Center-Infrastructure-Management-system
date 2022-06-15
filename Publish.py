from SimulatedIoT import TempratureSensor
from SimulatedIoT import HumiditySensor
from SimulatedIoT import MotionSensor
from SimulatedIoT import SmokeSensor

import time
from datetime import datetime
import json
import random
import paho.mqtt.client as mqtt


def read_temp():
    ts = TempratureSensor(20,10,15,30)
    dt = datetime.now().strftime("%d-%m-%YT%H:%M:%S")
    message = {
        "type-id": "Data Center " + ts.sensorType,
        "instance-id": ts.instanceID,
        "timestamp": dt,
        "value": {
            ts.unit: ts.sense()
        }
    }
    jmsg = json.dumps(message, indent=4)
    mqtt_publisher.publish('MainFrame/' + ts.sensorType + '/' + ts.instanceID, jmsg, 2)
    return jmsg

def read_hum():
    hs = HumiditySensor(45, 10, 15, 60)
    dt = datetime.now().strftime("%d-%m-%YT%H:%M:%S")
    message = {
        "type-id": "Data Center " + hs.sensorType,
        "instance-id": hs.instanceID,
        "timestamp": dt,
        "value": {
            hs.unit: hs.sense()
        }
    }
    jmsg = json.dumps(message, indent=4)
    mqtt_publisher.publish('MainFrame/' + hs.sensorType + '/' + hs.instanceID, jmsg, 2)
    return jmsg

############### MQTT section ##################

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(msg.topic+" "+message)


mqtt_publisher = mqtt.Client('Temperature publisher')
mqtt_publisher.on_connect = on_connect
mqtt_publisher.username_pw_set("username", "password")
mqtt_publisher.connect('192.168.0.112', 1883, 70)
mqtt_publisher.loop_start()

while True:
    temp_data = read_temp()
    hum_data = read_hum()
    print("Just Published " + str(temp_data) + " topic Sensor data" )
    print("Just Published " + str(hum_data) + " topic Sensor data")
    time.sleep(5)