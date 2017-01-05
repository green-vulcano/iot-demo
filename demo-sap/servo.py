import RPi.GPIO as GPIO
import time

class Servo:

    def __init__(self, id, name, gpio):
        self.id = id
        self.name = name
        self.gpio = gpio
        self.enable()
        print("servo '{0}' enabled".format(self.name))
    
    def enable(self):
    	GPIO.setmode(GPIO.BOARD)
    	GPIO.setup(self.gpio, GPIO.OUT)

    def disable(self):
    	GPIO.cleanup(self.gpio)

    	print("servo '{0}' disabled".format(self.name))

    def move(self, angle):
    	try:
    		print("moving servo '{0}' to angle {1}".format(self.name, angle))

    		self.pwm = GPIO.PWM(self.gpio, 100)
    		self.pwm.start(5)
    		duty = float(angle)/10 + 2.5  # angle to duty cycle conversion
    		self.pwm.ChangeDutyCycle(duty)
    		time.sleep(0.8)
    		self.pwm.stop()

    	except Exception as e:
    		print("error: " + str(e))
    		self.disable()