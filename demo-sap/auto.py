import threading
import time
import RPi.GPIO as GPIO

class Auto:

    def __init__(self, status=False):
        self.lightStatus = status
        self.t = threading.Thread(target=self.performLedAuto, args=("performLedAuto",))
        self.t.start()

        print(self.lightStatus)

    def performLedAuto(self, arg):
    	GPIO.setmode(GPIO.BOARD)
    	GPIO.setup(10, GPIO.OUT)
    	l1 = GPIO.PWM(10, 100) # 100 Hertz
    	l1.start(0)
    	ct = threading.currentThread()

    	while True:

    		if self.lightStatus:
    			print(self.lightStatus)
    			for i in range(101):
    				l1.ChangeDutyCycle(0 + i)
    				time.sleep(0.002)

    			for i in range(100, -1, -1):
    				l1.ChangeDutyCycle(0 + i)
    				time.sleep(0.002)

    			time.sleep(0.1)
    		else:
    			l1.ChangeDutyCycle(0)

    		if getattr(ct, "status", True):
    			self.lightStatus = True
    		else:
    			self.lightStatus = False

    def enable(self):
    	self.lightStatus = True

    def disable(self):
    	self.lightStatus = False

if __name__ == '__main__':
	 auto = Auto()
	 auto.disable()