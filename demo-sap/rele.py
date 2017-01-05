import RPi.GPIO as GPIO
import time

class Rele:

    def __init__(self, id, name, gpio):
        self.id = id
        self.name = name
        self.gpio = gpio
        self.enable()
        print("rele '{0}' enabled".format(self.name))
    
    def enable(self):
    	GPIO.setmode(GPIO.BOARD)
    	GPIO.setup(self.gpio, GPIO.OUT)

    def disable(self):
    	GPIO.cleanup(self.gpio)
    	print("rele '{0}' disabled".format(self.name))

    def on(self):
    	try:
    		print("turning rele '{0}' on".format(self.name))
    		GPIO.output(self.gpio, GPIO.HIGH)            
    	except Exception as e:
    		print("error: " + str(e))
    		self.disable()

    def off(self):
        try:
            print("turning rele '{0}' off".format(self.name))
            GPIO.output(self.gpio, GPIO.LOW)            
        except Exception as e:
            print("error: " + str(e))
            self.disable()