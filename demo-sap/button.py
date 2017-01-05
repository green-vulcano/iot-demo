import RPi.GPIO as GPIO
import time

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

class Button:

    def __init__(self, id, name, gpio, status=False):
        self.id = id
        self.name = name
        self.gpio = gpio
        self.status = status
        self.enable()

        print("button '{0}' status {1}".format(self.name, self.status))
    
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, bool):
            self._status = value
        else:
            raise TypeError("status must be a boolean")      
    
    def enable(self):
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.gpio, GPIO.RISING, callback=self._toggle, bouncetime=250)

    def disable(self):
    	GPIO.cleanup(self.gpio)
    	print("button '{0}' disabled".format(self.name))

    def _toggle(self, channel):
        if(GPIO.input(channel) == GPIO.HIGH):
            self.status = not self.status
            print("button '{0}' changes status to {1}".format(self.name, self.status))
            publish.single("gv/sensor/button/", "{{\"id\":\"{0}\",\"name\":\"{1}\",\"status\":\"{2}\"}}".format(self.id, self.name, self.status), hostname="localhost", protocol=mqtt.MQTTv31)