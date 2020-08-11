import pigpio as p
import time

isOpen = False

aufP = 13
aufM = 11
zuP = 18
zuM = 16
delay = 10

pi = pigpio.pi()

b = open()
if(b == True):
    print("Succesful")
    exit()
else:
    print("Fatal Exception")
    exit()

def clear():
    pi.write(aufP,0)
    pi.write(aufM,0)
    pi.write(zuP,0)
    pi.write(zuM,0)

def open():
    if(isOpen == False):
        pi.write(aufP,1)
        pi.write(aufM,1)
        time.sleep(delay)
        clear()
        isOpen = True
        return True
    else:
        return False

def close():
    if(isOpen == False):
        return False
    else:
        pi.write(zuP,1)
        pi.write(zuM,1)
        time.sleep(delay)
        clear()
        isOpen = False
        return True