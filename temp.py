import adafruit_dht
import time

s = adafruit_dht.DHT11(board.D21)

def readTemp():
    try:
        temp = tempSensor.temperature
        return temp
    except RuntimeError as e:
        print(e.args[0])
        return None

for i in range(3):
    t = readTemp()
    if t is not None:
        print("Temperatur: " + t)
    else:
        print("Error!")