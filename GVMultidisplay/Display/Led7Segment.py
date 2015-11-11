from Display import Display
import RPi.GPIO as GPIO

class Led7Segment(Display):

    #######################################################
    #
    #######################################################
    def __init__(self, name, cfg, charset):
        self.name = name
        self.text = ""
        self.charset = charset

        self.data_pin  = cfg["data"]
        self.clock_pin = cfg["clock"]
        self.latch_pin = cfg["latch"]

        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.setup(self.latch_pin, GPIO.OUT)

        self._digital_write(self.data_pin, 0)
        self._digital_write(self.clock_pin, 0)
        self._digital_write(self.latch_pin, 0)

    #######################################################
    #
    #######################################################
    def _digital_write(self, pin, value):
        if value == 1:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)

    #######################################################
    #
    #######################################################
    def _shift_bit(self, value):
        self._digital_write(self.data_pin, value)
        self._digital_write(self.clock_pin, 1)
        self._digital_write(self.clock_pin, 0)

    #######################################################
    #
    #######################################################
    def _latch(self):
        self._digital_write(self.latch_pin, 1)
        self._digital_write(self.latch_pin, 0)

    #######################################################
    #
    #######################################################
    def show(self, text, opt=None):
        if len(text) > 0:
            self.text = text[0].lower() # mostro solo un carattere
        else:
            self.text = " "

        try:
            if self.text in self.charset:
                value = self.charset[self.text]  
            else:
                value = self.charset[" "] 
                    
            tmp = str(bin(value))[2:]
            num = 8-len(tmp)
            valore = "0" * num + tmp
            
            for b in valore:
                self._shift_bit(bool(int(b)))
                self._latch()
        except Exception as e:
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
        self.text = " "
        self.show(self.text)