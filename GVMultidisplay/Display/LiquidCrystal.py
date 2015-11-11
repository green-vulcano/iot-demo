from Display import Display
import RPi.GPIO as GPIO
import time

class LiquidCrystal(Display):
	#######################################################
	#
	#######################################################    
	def __init__(self, name, cfg):
		self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
		self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

		# Timing constants
		self.E_PULSE = 0.0005
		self.E_DELAY = 0.0005

		self.name = name
		self._text_line1 = ""
		self._text_line2 = ""

		self.LCD_E = cfg["e"]
		self.LCD_RS = cfg["rs"]
		self.LCD_D4 = cfg["d4"]
		self.LCD_D5 = cfg["d5"]
		self.LCD_D6 = cfg["d6"]
		self.LCD_D7 = cfg["d7"]
		self.LCD_WIDTH = cfg["width"] # Maximum characters per line
		self.LCD_CHR = cfg["chr"]
		self.LCD_CMD = cfg["cmd"]

		GPIO.setup(self.LCD_E,  GPIO.OUT) # E
		GPIO.setup(self.LCD_RS, GPIO.OUT) # RS
		GPIO.setup(self.LCD_D4, GPIO.OUT) # DB4
		GPIO.setup(self.LCD_D5, GPIO.OUT) # DB5
		GPIO.setup(self.LCD_D6, GPIO.OUT) # DB6
		GPIO.setup(self.LCD_D7, GPIO.OUT) # DB7

		# Initialise display
		self._lcd_init()

	#######################################################
	# Initialise display
	#######################################################
	def _lcd_init(self):
		self._lcd_byte(0x33, self.LCD_CMD) # 110011 Initialise
		self._lcd_byte(0x32, self.LCD_CMD) # 110010 Initialise
		self._lcd_byte(0x06, self.LCD_CMD) # 000110 Cursor move direction
		self._lcd_byte(0x0C, self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
		self._lcd_byte(0x28, self.LCD_CMD) # 101000 Data length, number of lines, font size
		self._lcd_byte(0x01, self.LCD_CMD) # 000001 Clear display
		time.sleep(self.E_DELAY)
	
	#######################################################
	# Send byte to data pins
	#	bits = data
	#	mode = True for character, False for command
	#######################################################
	def _lcd_byte(self, bits, mode):
		GPIO.output(self.LCD_RS, mode) # RS

		# High bits
		GPIO.output(self.LCD_D4, False)
		GPIO.output(self.LCD_D5, False)
		GPIO.output(self.LCD_D6, False)
		GPIO.output(self.LCD_D7, False)

		if bits&0x10==0x10:
			GPIO.output(self.LCD_D4, True)
		if bits&0x20==0x20:
			GPIO.output(self.LCD_D5, True)
		if bits&0x40==0x40:
			GPIO.output(self.LCD_D6, True)
		if bits&0x80==0x80:
			GPIO.output(self.LCD_D7, True)

		# Toggle 'Enable' pin
		self._lcd_toggle_enable()

		# Low bits
		GPIO.output(self.LCD_D4, False)
		GPIO.output(self.LCD_D5, False)
		GPIO.output(self.LCD_D6, False)
		GPIO.output(self.LCD_D7, False)

		if bits & 0x01 == 0x01:
			GPIO.output(self.LCD_D4, True)
		if bits & 0x02 == 0x02:
			GPIO.output(self.LCD_D5, True)
		if bits & 0x04 == 0x04:
			GPIO.output(self.LCD_D6, True)
		if bits & 0x08 == 0x08:
			GPIO.output(self.LCD_D7, True)

		# Toggle 'Enable' pin
		self._lcd_toggle_enable()

	#######################################################
	# Toggle enable
	#######################################################
	def _lcd_toggle_enable(self):
		#time.sleep(self.E_DELAY)
		GPIO.output(self.LCD_E, True)
		time.sleep(0.0001)
		GPIO.output(self.LCD_E, False)
		#time.sleep(self.E_DELAY)

	#######################################################
	# Send string to display
	#######################################################
	def _lcd_string(self, message, line):
		message = message.ljust(self.LCD_WIDTH, " ")
		self._lcd_byte(line, self.LCD_CMD)

		for i in range(self.LCD_WIDTH):
			self._lcd_byte(ord(message[i]), self.LCD_CHR)

	#######################################################
	# opt = line number starting from 1
	#######################################################     
	def show(self, text, opt=None):
		if len(text) > 0: 
			if "\n" in text:
				sp = text.split('\n')
				self._text_line1 = sp[0]
				self._text_line2 = sp[1]
			else:
				self._text_line1 = text
				self._text_line2 = ""

			self._lcd_string(self._text_line1, self.LCD_LINE_1)
			self._lcd_string(self._text_line2, self.LCD_LINE_2)
	
	#######################################################
	#
	#######################################################          
	def getText(self):
		return self._text_line1 + "\n" + self._text_line2
	
	#######################################################
	#
	#######################################################     
	def clear(self):
		self._text_line1 = ""
		self._text_line2 = ""
		self._lcd_string(self._text_line1, self.LCD_LINE_1)
		self._lcd_string(self._text_line2, self.LCD_LINE_2)