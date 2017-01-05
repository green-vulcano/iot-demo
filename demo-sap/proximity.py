import RPi.GPIO as GPIO
import time

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

class Proximity:

    def __init__(self, id, name, gpio):
        self.id = id
        self.name = name
        self.gpio = gpio
        self.enable()
 
    def enable(self):
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.gpio, GPIO.RISING, callback=self._proximityCallback, bouncetime=250)

    def disable(self):
    	GPIO.cleanup(self.gpio)
    	print("proximity '{0}' disabled".format(self.name))

    def _proximityCallback(self, channel):
        if(GPIO.input(channel) == GPIO.HIGH):
            self.status = not self.status
            print("proximity '{0}'".format(self.name)
            publish.single("gv/sensor/proximity/"+str(self.id), "{{\"name\":\"{0}\",\"status\":\"{1}\"}}".format(self.name, True), hostname="localhost", protocol=mqtt.MQTTv31)