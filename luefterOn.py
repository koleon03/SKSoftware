import gpiozero
import time
import adafruit_bme280
import board
import busio



#Globale Variablen
isOpen = False
is2Open = False
luefterOn = False
aufP = "BOARD36"
aufM = "BOARD32"
zuP = "BOARD31"
zuM = "BOARD33"
lPin = "BOARD37"
delay = 5


#Initialisieren der Relais und Sensoren
relayAP = gpiozero.OutputDevice(pin=aufP, active_high=True, initial_value=False)
relayAM = gpiozero.OutputDevice(pin=aufM, active_high=True, initial_value=False)
relayZP = gpiozero.OutputDevice(pin=zuP, active_high=True, initial_value=False)
relayZM = gpiozero.OutputDevice(pin=zuM, active_high=True, initial_value=False)
relayL = gpiozero.OutputDevice(pin=lPin, active_high=True, initial_value=False)
i2c = busio.I2C(board.SCL, board.SDA)
tempSensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address = 0x76)

#Alle Relais ausschalten
def clear():
    relayAM.off()
    relayAP.off()
    relayZP.off()
    relayZM.off()

#Funktion zum Öffnen des Motors
def openMotor():
   
        relayAM.on()
        relayAP.on()
        time.sleep(delay)
        clear()
        isOpen = True
    

#Funktion zum Schließen des Motors
def closeMotor():  
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


def afterOpening(oldValue):
    global is2Open
    global luefterOn
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
    

relayL.on()
time.sleep(10)
