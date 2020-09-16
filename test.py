import gpiozero
import time
import adafruit_bme280
import board
import busio
import schedule
from guiGWM import Ui_main
from PyQt5 import QtWidgets, QtCore
import sys



aufP = "BOARD36"
aufM = "BOARD32"
zuP = "BOARD31"
zuM = "BOARD33"
lPin = "BOARD37"
delay = 5
tempWert = None
lfWert = None

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_main()
        self.ui.setupUi(self)
        self.button = self.findChild(QtWidgets.QPushButton, 'buttonOeffnen')
        self.button.clicked.connect(lambda: self.openMotor())
        self.button2 = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.button2.clicked.connect(lambda: self.closeMotor())
        tempWert = self.findChild(QtWidgets.QLabel, 'tempLabel')
        lfWert = self.findChild(QtWidgets.QLabel, 'label')
        self.threadpool = QtCore.QThreadPool()
        worker = Worker()
        self.threadpool.start(worker)
    
    def openMotor(self):
   
        relayAM.on()
        relayAP.on()
        time.sleep(delay)
        clear()
        isOpen = True
    
    def closeMotor(self):  
        relayZM.on()
        relayZP.on()
        time.sleep(delay)
        clear()
        isOpen = False

class WorkerSignals(QtCore.QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    '''
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)

class Worker(QtCore.QRunnable):
    
    isOpen = False
    is2Open = False
    luefterOn = False

    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        self.args = args
        self.kwargs = kwargs

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            tempC = readTemp()
            schedule.run_pending()
            if tempC is not None:
            #Temperaturvergleich
                if(tempC > 30):
                    if self.isOpen == False:
                        if(self.isOpen == False):
                            openMotor()
                            isOpen = True
                        self.afterOpening(tempC)
                elif(tempC < 25):
                    if isOpen == True:
                        closeMotor()
                        isOpen = False
    
    def afterOpening(self, oldValue):
        time.sleep(60)
        newValue = readTemp()
        if(newValue > oldValue):
            if(self.is2Open == False):
                openMotor()
                self.is2Open = True
            if(self.luefterOn == False):
                relayL.on()
                self.luefterOn = True
            afterOpening(newValue)
        elif(newValue > 30):
            if(self.is2Open == False):
                openMotor()
                self.is2Open = True
            if(self.luefterOn == True):
                relayL.off()
            afterOpening(newValue)
        elif(newValue < 30):
            if(self.is2Open == True):
                closeMotor()
                self.is2Open = False
            if(self.luefterOn == True):
                relayL.off()
                self.luefterOn = False



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
       # print(temp)
        return temp
    except RuntimeError as e:
        print(e.args[0])
        return None




def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()


    



