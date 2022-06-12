from SimulatedIoT import TempratureSensor
from SimulatedIoT import HumiditySensor
import time
import random
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

Broker = "192.168.1.252"

sub_topic = "sensor/instructions"    # receive messages on this topic

pub_topic = "sensor/data"       # send messages to this topic


############### sensehat inputs ##################
def read_temp():
    ts = TempratureSensor(20,10,15,30)
    return ts

def read_humi():
    hs = HumiditySensor(45, 10, 15, 60)
    return hs

def read_motion():
    # Sensor state simulation(0 or 1)
    m_sensor = random.randint(0, 1)
    return m_sensor

def read_smoke():
    # Sensor state simulation(0 or 1)
    S_sensor = random.randint(0, 1)
    return S_sensor

############### MQTT section ##################

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(msg.topic+" "+message)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)
client.loop_start()

while True:
    sensor_data = [read_temp(), read_humi(), read_motion(), read_smoke() ]
    client.publish("monto/solar/sensors", str(sensor_data))
    time.sleep(1*60)