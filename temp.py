import adafruit_dht
import time
import board

s = adafruit_dht.DHT11(board.)

def readTemp():
    try:
        temp = tempSensor.temperature
        print(temp)
        return temp
    except RuntimeError as e:
        print(e.args[0])
        return None

