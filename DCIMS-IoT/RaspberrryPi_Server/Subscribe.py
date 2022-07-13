#Importing all libraries
import paho.mqtt.client as mqtt
import ssl
import json
from ProblemFileGenerator import  GenerateProblemPDDLFile
from ProblemFileGenerator import GetAIPlan


def on_connect(client, userdata, flags, rc):                                # Funcition for establishing connection
    print("Connected with result code "+str(rc))

def on_connect_act(client, userdata, flags, rc):
    print("Connected to AWS")
    print("Connected with result code " + str(rc))

def on_message(client, userdata, message):                                  # Funcition for sending msg
    global Temperature, Humidity, FireAlrm, servo, MotionAlrm, buzzer
    msg = (json.loads(message.payload.decode("utf-8"))) #Loading the
    Temp = round(msg.get('Temperature'))
    Humi = round(msg.get('Humidity'))
    smoke = (msg.get('FireAlarm'))
    motion =(msg.get('Motion'))

    if (0 < Temp <= 17):
        Temperature = 'cool'
    elif (18 < Temp <= 24):
        Temperature = "normal"
    elif (Temp > 25) :
        Temperature = "Hot"

    if 0 < Humi <= 40:
        Humidity = "Dry"
    elif 41 < Humi <= 61:
        Humidity = "normal"
    elif Humi > 61:
        Humidity = "Wet"

    if motion=="Alarm":
        buzzer = "on"
        motionalrm = True
    else:
        buzzer = "off"
        motionalrm = False
        
    if smoke=="Alarm":
        smokealrm = True
        servo = "on"
        buzzer = "on"
    else:
        smokealrm = False
        servo = "off"
        buzzer = "off"
     

    def action():
        global Fan, condition, Fan_A, servo_A, Buzzer_A

        #Fuzzy logic for Tempereature  and humidity control
        if (Temperature == "cool" and Humidity == "Dry"):
            Fan = "Low"
            condition = "cool"
        elif Temperature == "normal" and Humidity == "Dry":
            Fan = "Medium"
            condition = "cool"
        elif Temperature == "Hot" and Humidity == "Dry":
            Fan = "High"
            condition = "cool"
        if Temperature == "cool" and Humidity == "normal":
            Fan = "Low"
            condition = "normal"
        elif Temperature == "normal" and Humidity == "normal":
            Fan = "Medium"
            condition = "normal"
        elif Temperature == "Hot" and Humidity == "normal":
            Fan = "High"
            condition = "normal"
        if Temperature == "cool" and Humidity == "Wet":
            Fan = "Low"
            condition = "Dry"
        elif Temperature == "normal" and Humidity == "Wet":
            Fan = "Medium"
            condition = "Dry"
        elif Temperature == "Hot" and Humidity == "Wet":
            Fan = "High"
            condition = "Dry"

        #call Problem file generator script
        GenerateProblemPDDLFile(motionalrm, smokealrm, Fan)
        GetAIPlan()                                                                     #call for AI plan
        f = open("/home/pi/DCIMS-IoT/AI_Planning/AI_Plan/AIPlan.txt", "r")              #save it on the local drive
        contents = f.readlines()

        #Decrypting AI plan for actions
        if (contents[0].strip() == "(motion_detection off)"):
            Buzzer_A = "off"
        elif (contents[0].strip() == "(motion_detection on)"):
            Buzzer_A = "on"
        if (contents[1].strip() == "(alarm off)"):
            servo_A = "off"
        elif (contents[1].strip() == "(alarm on)"):
            servo_A = "on"
        if (contents[2].strip() == "(fan prev off)"):
            Fan_A = "off"
        elif (contents[2].strip() == "(fan prev low)"):
            Fan_A = "Low"
        elif (contents[2].strip() == "(fan prev medium)"):
            Fan_A = "Medium"
        elif (contents[2] == "(fan prev high)"):
            Fan_A = "High"

        message = {
            "Area-id": "Data Center-1",
            "Fan":Fan,
            "Condition":condition,
            "Servo": servo,
            "Buzzer":buzzer,
            "Fan_A": Fan_A,
            "Servo_A": servo_A,
            "Buzzer_A": Buzzer_A
        }                                                       #message

        jmsg = json.dumps(message, indent=4)
        mqtt_publisher.publish("Area-1/Action", jmsg, 1)        #Topic:Area-1/Action to publish for Actions values
    action()

mqtt_subscriber = mqtt.Client()                                 #mqtt subscriber object
mqtt_subscriber.on_connect = on_connect                         #assign on_connect function
mqtt_subscriber.on_message = on_message                         #assign on_message function
awshost = "xxxxxxxxxxxxxx-ats.iot.us-east-1.amazonaws.com"      #Endpoint
awsport = 8883                                                  #Port no.

caPath = "/home/pi/DCIMS-IoT/AWSIoT/Root-CA.pem"                # Root_CA_Certificate_Name
certPath = "/home/pi/DCIMS-IoT/AWSIoT/certificate.pem.crt"      # <Thing_Name>.cert.pem
keyPath = "/home/pi/DCIMS-IoT/AWSIoT/private.pem.key"           # <Thing_Name>.private.key

mqtt_subscriber.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)                                     # pass parameters
mqtt_subscriber.username_pw_set("username", "xxxxxx")
mqtt_subscriber.connect(awshost, awsport, keepalive=60)         # connect to aws server
mqtt_subscriber.subscribe('Area-1/Sensor_Data', qos=1)          #Topic:Area-1/Sensor_Data to subscribe for sensor values

mqtt_publisher = mqtt.Client()                                  #mqtt publisher object
mqtt_publisher.on_connect = on_connect                          #assign on_connect function
mqtt_publisher.on_message = on_message                          #assign on_message function

mqtt_publisher.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)                                     # pass parameters
mqtt_publisher.username_pw_set("username", "xxxxxx")
mqtt_publisher.connect(awshost, awsport, keepalive=60)          # connect to aws server

mqtt_publisher.loop_start()                                     # Start the loop

while True:
    mqtt_subscriber.loop_start()                                # Start the loop