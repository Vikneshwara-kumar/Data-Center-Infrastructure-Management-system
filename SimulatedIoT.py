from random import random

class TempratureSensor:
    sensorType="temperature"
    instanceID="52ks563ks"
    unit ="celsius"
    def __init__(self,averageTemprature, tempratureVariation, minTemprature, maxTemprature):
        self.averageTemperature = averageTemprature
        self.tempratureVariation = tempratureVariation
        self.minTemperature = minTemprature
        self.maxTemperature = maxTemprature
    def sense(self):
        self.value = self.complexRandom()
        return self.value

    def simpleRandom(self):
        value = self.minTemperature + (random()*((self.maxTemperature - self.minTemperature)))
        return value

    def complexRandom(self):
        value = self.averageTemperature*(1+((self.tempratureVariation/100)*(3*random()-1)))
        value = max(value,self.minTemperature)
        value = min(value,self.maxTemperature)
        return value

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