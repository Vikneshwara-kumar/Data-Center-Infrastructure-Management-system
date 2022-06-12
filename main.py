import time
import threading
import random
from SimulatedIoT import TempratureSensor
from SimulatedIoT import HumiditySensor
# Periodic execution processing




def IoT():
    ts = TempratureSensor(20,10,15,30)
    print(ts.sensorType,ts.sense())
    TS=ts.sense()
    if TS >= 24.0:
        print("Temp is high")
    elif TS <16:
        print("Temp is low")

    hs = HumiditySensor(45, 10, 15, 60)
    print(hs.sensorType, hs.sense(), hs.unit)
    HS=hs.sense()
    if HS >= 50.0:
        print("Temp is high")
    elif HS < 40:
        print("Temp is low")

    # Sensor state simulation(0 or 1)
    m_sensor = random.randint(0, 1)
    print("Motion:",m_sensor)
    if m_sensor==1:
        print("Motion Detected")

    # Sensor state simulation(0 or 1)
    S_sensor = random.randint(0, 1)
    print("Smoke:", S_sensor)
    if S_sensor==1:
        print("Fire Alert")


def scheduler(interval, f, wait=True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target=f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)


if __name__ == "__main__":
    # Periodic execution setting(3 second intervals)
    scheduler(5, IoT, True)