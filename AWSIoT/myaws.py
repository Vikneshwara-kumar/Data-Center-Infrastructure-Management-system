import time
from SimulatedIoT import TempratureSensor
from SimulatedIoT import HumiditySensor
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
from datetime import datetime
import json
import paho.mqtt.client as mqtt


myMQTTClient = AWSIoTMQTTClient("VickyClientID")  # random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("a1l83aslu1wtwg-ats.iot.us-east-1.amazonaws.com", 8883)

myMQTTClient.configureCredentials("C:/Users/vikne/PycharmProjects/DCIMS-IoT/AWSIoT/Root-ca.pem", "C:/Users/vikne/PycharmProjects/DCIMS-IoT/AWSIoT/private.pem.key",
                                  "C:/Users/vikne/PycharmProjects/DCIMS-IoT/AWSIoT/certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
print('Initiating Realtime Data Transfer From Raspberry Pi...')

myMQTTClient.connect()

def Sensor_monitor():
    ts = TempratureSensor(20,10,15,30)
    hs = HumiditySensor(45, 10, 15, 60)
    dt = datetime.now().strftime("%d-%m-%YT%H:%M:%S")
    message ={
            "Area-id": "Data Center-1",
            "instance-id": ts.instanceID,
            "timestamp": dt,
            "Temperature": ts.sense(),
            "Humidity": hs.sense()
        }
    jmsg = json.dumps(message, indent=4)
    myMQTTClient.publish(
        topic="Area-1",
        QoS=1,
        payload=jmsg)
    return jmsg

############### MQTT section ##################

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(msg.topic+" "+message)


mqtt_publisher = mqtt.Client('Area-1 publisher')
mqtt_publisher.on_connect = on_connect
mqtt_publisher.username_pw_set("username", "password")
mqtt_publisher.connect('192.168.0.112', 1883, 70)
mqtt_publisher.loop_start()

while True:
    Sensor_monitor()
    print("Just Published " + str(Sensor_monitor()) + " topic Sensor data")
    time.sleep(5)





