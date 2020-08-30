import gpiozero
import time
import adafruit_bme280
import board
import busio
import PySimpleGUI as sg


#Globale Variablen
isOpen = False
aufP = "BOARD36"
aufM = "BOARD32"
zuP = "BOARD31"
zuM = "BOARD33"
delay = 5


#Initialisieren der Relais und Sensoren
relayAP = gpiozero.OutputDevice(pin=aufP, active_high=True, initial_value=False)
relayAM = gpiozero.OutputDevice(pin=aufM, active_high=True, initial_value=False)
relayZP = gpiozero.OutputDevice(pin=zuP, active_high=True, initial_value=False)
relayZM = gpiozero.OutputDevice(pin=zuM, active_high=True, initial_value=False)
i2c = busio.I2C(board.SCL, board.SDA)
tempSensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address = 0x76)
sg.theme('DarkAmber')	# Add a touch of color
tempText = sg.Text("0")
# All the stuff inside your window.

layout = [ [sg.Text("Temperatur: "), tempText] ]

# Create the Window
window = sg.Window('Test', layout, size=(1920,1080))


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
        print(temp)
        return temp
    except RuntimeError as e:
        print(e.args[0])
        return None

print("1")
#Hauptschleife
while True:
    print("2")
    print("3")
    tempC = readTemp()
    print("4")
    tempText.update(value=tempC)
    if tempC is not None:
        #Temperaturvergleich
        if(tempC > 30):
            if isOpen == False:
                openMotor()
        elif(tempC < 25):
            if isOpen == True:
                closeMotor()
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    
window.close()



