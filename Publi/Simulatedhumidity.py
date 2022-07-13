from random import random

class HumiditySensor:
    sensorType="humidity"
    instanceID="53ks564ks"
    unit ="%"
    def __init__(self,averageHumidity, HumidityVariation, minHumidity, maxHumidity):
        self.averageHumidity = averageHumidity
        self.HumidityVariation = HumidityVariation
        self.minHumidity = minHumidity
        self.maxHumidity = maxHumidity
    def sense(self):
        self.value = self.complexRandom()
        return self.value

    def simpleRandom(self):
        value = self.minHumidity + (random()*((self.maxHumidity - self.minHumidity)))
        return value

    def complexRandom(self):
        value = self.averageHumidity*(1+((self.HumidityVariation/100)*(3*random()-1)))
        value = max(value,self.minHumidity)
        value = min(value,self.maxHumidity)
        return value
