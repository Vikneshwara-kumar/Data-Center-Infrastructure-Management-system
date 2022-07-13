import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, message):
    print('Message topic {}'.format(message.topic))
    print('Message payload:')
    print(json.loads(message.payload.decode()))

mqtt_subscriber = mqtt.Client('Temperature subscriber')
mqtt_subscriber.on_message = on_message
mqtt_subscriber.on_connect = on_connect
mqtt_subscriber.username_pw_set("username", "password")

mqtt_subscriber.connect('192.168.0.112', 1883, 70)
#mqtt_subscriber.subscribe('u38/0/353/+/temperature/+', qos=2)
mqtt_subscriber.subscribe('MainFrame/Temperature', qos=2)
mqtt_subscriber.subscribe('MainFrame/Humidity', qos=2)
#mqtt_subscriber.subscribe('u38/0/353/+/humididty/+', qos=2)

mqtt_subscriber.loop_forever()