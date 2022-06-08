import time
import threading
import random
from random import seed
from random import randint


# Periodic execution processing
def Sensors():
    # Temperature simulation(25 degrees+α)
    now = time.time()
    print(now%5)
    temp = 15 + now % 3 + (now / 10) % 10
    # Truncate to two decimal places
    str = "{0:.0f}".format(temp)
    temp = float(str)
    print("Temprature:",temp)

    # Sensor state simulation(0 or 1)
    m_sensor = random.randint(0, 1)
    print("Motion:",m_sensor)

    # Humidity simulation(25 degrees+α)
    hum = 30 + now % 3 + (now / 10) % 10
    # Truncate to two decimal places
    strh = "{0:.0f}".format(hum)
    hum = float(strh)
    print("Humidity:",hum)

    if temp >= 24.0:
        print("Temp is high")
    elif temp <13:
        print("Temp is low")

    if m_sensor==1:
        print("Motion Detected")


# Periodic execution setting processing
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
    scheduler(3, Sensors, True)