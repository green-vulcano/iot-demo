# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json

import threading
import time

from servo import Servo
from button import Button
from proximity import Proximity
from led import Led
from rele import Rele

##############################################################
# TOPICS & PAYLOADS
#	gv/sensor/button {"id":"btn1","status":"False", "name":"galleria"}
#	gv/sensor/servo {"id":"srv1","angle":"120", "name":"galleria"}
#   gv/sensor/led {"id":"led1","status":"on", "name":"galleria"}
#   gv/sensor/rele {"id":"rele","status":"on", "name":"galleria"}

servo1 = Servo("srv1", "servo_tombino", 26)
servo2 = Servo("srv2", "servo_albero", 22)
servo3 = Servo("srv3", "servo_segnale", 24)

button1 = Button("btn1", "button_rele", 11)
button2 = Button("btn2", "button_albero", 13)
button3 = Button("btn3", "button_segnale", 15)
button4 = Button("btn4", "button_tombino", 19)
button5 = Button("btn5", "button_galleria", 21)

proximity1 = Proximity("prx1", "proximity_albero", 29)
proximity2 = Proximity("prx2", "proximity_segnale", 31)
proximity3 = Proximity("prx3", "proximity_fumo", 33)
proximity4 = Proximity("prx4", "proximity_tombino", 35)
proximity5 = Proximity("prx5", "proximity_galleria", 37)

led1 = Led("led1", "led_galleria", 12)
led2 = Led("led2", "led_auto1", 10)

rele1 = Rele("rele1", "rele_power", 23)

#################################################################################
#
# 
#################################################################################
def performLedAuto(arg):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(10, GPIO.OUT)
	l1 = GPIO.PWM(10, 100) # 100 Hertz
	l1.start(0)

	t = threading.currentThread()
	lightStatus = False

	while True:

		if lightStatus:
			for i in range(101):
				l1.ChangeDutyCycle(0 + i)
				time.sleep(0.002)

			for i in range(100, -1, -1):
				l1.ChangeDutyCycle(0 + i)
				time.sleep(0.002)

			time.sleep(0.1)
		else:
			l1.ChangeDutyCycle(0)

		if getattr(t, "status", True):
			lightStatus = True

		else:
			lightStatus = False

auto_t = threading.Thread(target=performLedAuto, args=("performLedAuto",))
auto_t.status = False
auto_t.start()

#################################################################################
#
# The callback for when the client receives a CONNACK response from the server.
#################################################################################
def on_connect(client, userdata, rc):
	client.subscribe("gv/sensor/#")
	client.subscribe("gv/req/status")
	client.publish("gv/connection", "{\"status\":\"true\"}", 0, False)

#################################################################################
#
#
#################################################################################
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("mqtt client: unexpected disconnection")
    else:
    	print("mqtt client: disconnected")

#################################################################################
#
# The callback for when a PUBLISH message is received from the server.
#################################################################################
def on_message(client, userdata, msg):

	try:
		strPayload = msg.payload.decode()
		jsonMsg = json.loads(strPayload)

		if msg.topic == "gv/sensor/button":
			performButton(jsonMsg)
		elif msg.topic == "gv/sensor/servo":
			performServo(jsonMsg)
		elif msg.topic == "gv/sensor/led":
			performLed(jsonMsg)
		elif msg.topic == "gv/sensor/rele":
			performRele(jsonMsg)
		elif msg.topic == "gv/req/status":
			performStatus()

	except Exception as e:
		print("Exception: " + str(e))

#################################################################################
#
# 
#################################################################################
def performStatus():
	topic = "gv/status"
	payload = "{{\"btn1\":\"{0}\",\"btn2\":\"{1}\",\"btn3\":\"{2}\",\"btn4\":\"{3}\",\"btn5\":\"{4}\"}}".format(str(button1.status),str(button2.status),str(button3.status),str(button4.status),str(button5.status))
	publish.single(topic, payload, hostname="localhost", protocol=mqtt.MQTTv31)


#################################################################################
#
# 
#################################################################################
def performServo(payload):
	
	id = str(payload["id"])
	angle = str(payload["angle"])

	if id == "srv1":
		servo1.move(angle)
	elif id == "srv2":
		servo2.move(angle)
	elif id == "srv3":
		servo3.move(angle)
	else:
		print("Unknown servo id " + str(id))

#################################################################################
#
# 
#################################################################################
def performButton(payload):
	id = str(payload["id"])
	name = str(payload["name"])
	status = str(payload["status"])

	# albero
	if id == "btn2":
		if status in ['true', 'True']:
			servo2.move("160")
		else:
			servo2.move("120")
	# segnale
	elif id == "btn3":
		if status in ['true', 'True']:
			servo3.move("50")
		else:
			servo3.move("0")
	# tombino
	elif id == "btn4":
		if status in ['true', 'True']:
			servo1.move("120")
		else:
			servo1.move("160")
	#galleria
	elif id == "btn5":
		if status in ['true', 'True']:
			led1.on()
		else:
			led1.off()	
	# led auto-rele
	elif id == "btn1":
		if status in ['true', 'True']:
			auto_t.status = True
			rele1.on()
		else:
			auto_t.status = False
			rele1.off()
#################################################################################
#
# 
#################################################################################
def performLed(payload):
	id = str(payload["id"])
	name = str(payload["name"])
	status = str(payload["status"])

	# galleria
	if id == "led1":
		if status in ['true', 'True', 'on', 'On']:
			led1.on()
		else:
			led1.off()
	elif id == "led2":
		if status in ['true', 'True', 'on', 'On']:
			led2.on()
		else:
			led2.off()
	# elif id == "led3":
	# 	if status in ['true', 'True', 'on', 'On']:
	# 		led3.on()
	# 	else:
	# 		led3.onff()

#################################################################################
#
# 
#################################################################################
def performRele(payload):
	id = str(payload["id"])
	name = str(payload["name"])
	status = str(payload["status"])

	if id == "rele1":
		if status in ['true', 'True', 'on', 'On']:
			rele1.on()
		else:
			rele1.off()		

#################################################################################
#
#
#################################################################################
def main():
	try:
		client = mqtt.Client()
		client.on_connect = on_connect
		client.on_message = on_message
		client.on_disconnect = on_disconnect

		client.will_set('gv/connetion', "{\"status\":\"false\"}", 0, False)
		client.connect("localhost", 1883, 60)

		servo1.move("120")
		servo2.move("160")
		servo3.move("50")
		led1.on()
		
		button1.status = False # rele
		button2.status = True # albero
		button3.status = True # segnale
		button4.status = True # tombino
		button5.status = True # galleria
		
		client.loop_forever()
	except KeyboardInterrupt:
		client.disconnect()

		GPIO.cleanup()

		auto_t.join()

		print("Bye bye")
	except Exception as e:
		print("Unexpected exit: " + str(e))

#################################################################################
#
#
#################################################################################
if __name__ == '__main__':
	 main()
