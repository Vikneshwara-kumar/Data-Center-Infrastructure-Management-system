import time
from datetime import datetime
import json
from SimulatedIoT import TempratureSensor
import paho.mqtt.client as mqtt

class Simulator:
    def __init__(self, interval):
        self.interval = interval
    def start(self):
        ts = TempratureSensor(20, 10, 16, 35)
        mqtt_publisher = mqtt.Client('Temperature publisher')
        mqtt_publisher.connect('127.0.0.1', 1883, 70)
        mqtt_publisher.loop_start()
        while True:
            dt = datetime.now().strftime("%d-%m-%YT%H:%M:%S")
            message = {
                "type-id": "de.uni-stuttgart.iaas.sc." + ts.sensorType,
                "instance-id": ts.instanceID,
                "timestamp": dt,
                "value": {
                    ts.unit: ts.sense()
                }
            }
            jmsg = json.dumps(message, indent=4)
            mqtt_publisher.publish('u38/0/353/window/' + ts.sensorType + '/' + ts.instanceID, jmsg, 2)
            time.sleep(self.interval)
s = Simulator(5)
s.start()