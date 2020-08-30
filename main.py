import gpiozero
import time
import adafruit_bme280


#Globale Variablen
isOpen = False
aufP = "BOARD13"
aufM = "BOARD11"
zuP = "BOARD18"
zuM = "BOARD16"
delay = 5

#Initialisieren der Relais und Sensoren
relayAP = gpiozero.OutputDevice(pin=aufP, active_high=True, initial_value=False)
relayAM = gpiozero.OutputDevice(pin=aufM, active_high=True, initial_value=False)
relayZP = gpiozero.OutputDevice(pin=zuP, active_high=True, initial_value=False)
relayZM = gpiozero.OutputDevice(pin=zuM, active_high=True, initial_value=False)
tempSensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address = 0x76)


#Alle Relais ausschalten
def clear():
    relayAM.off()
    relayAP.off()
    relayZP.off()
    relayZM.off()

#Funktion zum Öffnen des Motors
def openMotor():
    global isOpen
    if(isOpen == False):
        relayAM.on()
        relayAP.on()
        time.sleep(delay)
        clear()
        isOpen = True
        return True
    else:
        return False

#Funktion zum Schließen des Motors
def closeMotor():
    global isOpen
    if(isOpen == False):
        return False
    else:
        relayZM.on()
        relayZP.on()
        time.sleep(delay)
        clear()
        isOpen = False
        return True

#Funktion zum Auslesen der Temperatur
def readTemp():
    try:
        temp = tempSensor.temperature
        print("Read the temperature at " + temp + "C")
        return temp
    except RuntimeError as e:
        print(e.args[0])
        return None


#Hauptschleife
while True:
    time.sleep(120)
    tempC = readTemp()
    if tempC is not None:
        #Temperaturvergleich
        if(tempC > 25):
            if isOpen == False:
                openMotor()
        elif(tempC < 20):
            if isOpen == True:
                closeMotor()
                



