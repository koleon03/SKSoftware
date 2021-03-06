import gpiozero
import time
import adafruit_bme280
import board
import busio
import schedule
from guiGWM import Ui_main
from PyQt5 import QtWidgets, QtCore
import sys
import pandas as pd

aufP = "BOARD36"
aufM = "BOARD32"
zuP = "BOARD31"
zuM = "BOARD33"
lPin = "BOARD37"
delay = 5
timedData = 0
isOpen = False
is2Open = False
luefterOn = False
dataList = []
data = pd.DataFrame({
    "Temperature": [],
    "Time": []
})


relayAP = gpiozero.OutputDevice(pin=aufP, active_high=True, initial_value=False)
relayAM = gpiozero.OutputDevice(pin=aufM, active_high=True, initial_value=False)
relayZP = gpiozero.OutputDevice(pin=zuP, active_high=True, initial_value=False)
relayZM = gpiozero.OutputDevice(pin=zuM, active_high=True, initial_value=False)
relayL = gpiozero.OutputDevice(pin=lPin, active_high=True, initial_value=False)
i2c = busio.I2C(board.SCL, board.SDA)
tempSensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address = 0x76)

class Worker2(QtCore.QRunnable):
    def __init__(self, *args, **kwargs):
        super(Worker2, self).__init__()
        self.args = args
        self.kwargs = kwargs

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


threadPool = QtCore.QThreadPool()
worker = Worker2()
threadPool.start(worker)

#Alle Relais ausschalten
def clear():
    relayAM.off()
    relayAP.off()
    relayZP.off()
    relayZM.off()

#Funktion zum Öffnen des Motors
def openMotor():
    global delay
    global isOpen
    relayAM.on()
    relayAP.on()
    time.sleep(delay)
    clear()
    isOpen = True
    

#Funktion zum Schließen des Motors
def closeMotor():  
    global delay
    global isOpen
    relayZM.on()
    relayZP.on()
    time.sleep(delay)
    clear()
    isOpen = False
     

#Funktion zum Auslesen der Temperatur
def readTemp():
    try:
        temp = tempSensor.temperature
        print(temp)
        return temp
    except RuntimeError as e:
        print(e.args[0])
        return None

def readLF():
    try:
        lf = tempSensor.humidity
        return lf
    except RuntimeError as e:
        print(e.args[0])
        return None

def afterOpening(oldValue):
    global is2Open
    global luefterOn
    global isOpen
    time.sleep(60)
    newValue = readTemp()
    if(newValue > oldValue):
        if(is2Open == False):
            openMotor()
            is2Open = True
        if(luefterOn == False):
            relayL.on()
            luefterOn = True
        afterOpening(newValue)
    elif(newValue > 30):
        if(is2Open == False):
            openMotor()
            is2Open = True
        if(luefterOn == True):
            relayL.off()
        afterOpening(newValue)
    elif(newValue < 30):
        if(is2Open == True):
            closeMotor()
            is2Open = False
        if(luefterOn == True):
            relayL.off()
            luefterOn = False

def addData():
    global timedData
    print("Executed!")
    if(timedData > 1200):
        df = pd.DataFrame(dataList, columns=['Temperature', 'Time'])
        df.to_excel('data.xlsx', sheet_name='Temperaturdaten', index=False)
        sys.exit(0)
    t = readTemp()
    dataList.append([t, timedData])
    timedData = timedData + 10


schedule.every(10).seconds.do(addData)
addData()
while True:
    schedule.run_pending()

