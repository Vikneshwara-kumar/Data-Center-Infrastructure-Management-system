import time
from SimulatedIoT import TempratureSensor
from SimulatedIoT import HumiditySensor
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
from datetime import datetime
import json
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    a = msg.topic
    if a == "Sensor_Data":
        t = json.loads(str(msg.payload.decode("utf-8")))
        print(t)


myMQTTClient = AWSIoTMQTTClient("VickyClientID")  # random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("a1l83aslu1wtwg-ats.iot.us-east-1.amazonaws.com", 8883)

myMQTTClient.configureCredentials("C:/Users/vikne/PycharmProjects/DCIMS-IoT/AWSIoT/Root-ca.pem", "C:/Users/vikne/PycharmProjects/DCIMS-IoT/AWSIoT/private.pem.key",
                                  "C:/Users/vikne/PycharmProjects/DCIMS-IoT/AWSIoT/certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
print('Initiating IoT Core Topic....')
myMQTTClient.connect()
myMQTTClient.subscribe("Area-1", 2, on_message)

