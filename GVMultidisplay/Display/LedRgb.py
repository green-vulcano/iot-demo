from Display import Display
import RPi.GPIO as GPIO

class LedRgb(Display):

    #######################################################
    #
    #######################################################
    def __init__(self, name, cfg, colorset):
        self.name = name
        self.colorset = colorset
        self.text = "off"

        self.red_pin = cfg["red"]
        self.green_pin = cfg["green"]
        self.blue_pin = cfg["blue"]

        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

        #---------------------------------------------------
        # set pwm mode, at 100 hertz
        #---------------------------------------------------
        self.red_led = GPIO.PWM(self.red_pin, 100)
        self.green_led = GPIO.PWM(self.green_pin, 100)
        self.blue_led = GPIO.PWM(self.blue_pin, 100)

    #######################################################
    #
    #######################################################
    def show(self, text, opt="hex"):
        try:
            if (opt == None or opt == "hex") and self._isHex(text):
                self._applyColor(text)

            elif opt == "txt" and text in self.colorset:
                    color_text = self.colorset[text]
                    self._applyColor(color_text)
            else:
                print("color value uncorrect: %s" %str(text))
                #self._applyColor(self.colorset["off"])

        except Exception as e:
            print("show exception")
            print("Exception: %s" %str(e.args[0]))

    #######################################################
    #
    #######################################################
    def getText(self):
        return self.text

    #######################################################
    #
    #######################################################
    def clear(self):
        self.text = "off"
        self.show(self.text, opt="txt")

    #######################################################
    #
    #######################################################
    def _applyColor(self, hex_value):
        #---------------------------------------------------
        # start led on 0 percent duty cycle(off)
        #---------------------------------------------------
        self.red_led.start(0)
        self.green_led.start(0)
        self.blue_led.start(0)

        #---------------------------------------------------
        # select rgb couple
        #---------------------------------------------------
        r = hex_value[0:2]
        g = hex_value[2:4]
        b = hex_value[4:6]

        #---------------------------------------------------
        # convert from string/hex(value from 0x00 to 0xff)
        # to dec (value from 0 to 100)
        #---------------------------------------------------
        red     = ((int(int(r, 16)) / 255.0) * 100)
        green   = ((int(int(g, 16)) / 255.0) * 100)
        blue    = ((int(int(b, 16)) / 255.0) * 100)

        #---------------------------------------------------
        # apply the duty cycle
        #---------------------------------------------------
        self.red_led.ChangeDutyCycle(red)
        self.green_led.ChangeDutyCycle(green)
        self.blue_led.ChangeDutyCycle(blue)

    def _isHex(self, s):
        try:
            if len(s) == 6:
                int(s, 16)
                return True
        except ValueError:
            return False




