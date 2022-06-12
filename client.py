import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

Broker = "192.168.0.112"

sub_topic = "sensor/data"    # receive messages on this topic



# mqtt section

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    message = str(msg.payload.decode("utf-8"))
    #print(msg.topic + " " +message)
    print("Received message:", +message)

client = mqtt.Client("PC")
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 80)
client.loop_forever()