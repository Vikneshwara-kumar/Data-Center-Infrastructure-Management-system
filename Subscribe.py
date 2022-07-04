import paho.mqtt.client as mqtt
import ssl
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, message):
    print('Message topic {}'.format(message.topic))
    print('Message payload:')
    msg = (json.loads(message.payload.decode("utf-8")))
    print(json.loads(message.payload.decode("utf-8")))
    Temp = round(msg.get('Temperature'))
    Humi  = round(msg.get('Humidity'))
    Motion = (msg.get('Motion-Detector'))
    print(Temp)
    print(Humi)
    print(Motion)


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
mqtt_subscriber.subscribe('Area-1', qos=1)

mqtt_subscriber.loop_forever()