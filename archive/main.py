import gpiozero
import time

isOpen = False

aufP = "BOARD36"
aufM = "BOARD32"
zuP = "BOARD31"
zuM = "BOARD33"
delay = 5

relayAP = gpiozero.OutputDevice(pin=aufP, active_high=True, initial_value=False)
relayAM = gpiozero.OutputDevice(pin=aufM, active_high=True, initial_value=False)
relayZP = gpiozero.OutputDevice(pin=zuP, active_high=True, initial_value=False)
relayZM = gpiozero.OutputDevice(pin=zuM, active_high=True, initial_value=False)



def clear():
    relayAM.off()
    relayAP.off()
    relayZP.off()
    relayZM.off()

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

openMotor()
time.sleep(2)
closeMotor()
