from gv import GVComm, DeviceInfo, DefaultProtocol
from gv.transports.mqtt import MqttTransport

from Display import Led7Segment, Led7SegmentCluster, LiquidCrystal, LedRgb
from config import cfg, charset, colorset
import RPi.GPIO as GPIO
from time import sleep
import json
from threading import Thread
import sys
import os

device_config = cfg["device"]
devInfo = DeviceInfo(id_=device_config["id"], name=device_config["name"], ip=device_config["ip"], port=9999)
mqtt = MqttTransport(device_info=devInfo, server=device_config["server_ip"], port=1883)
proto = DefaultProtocol(transport=mqtt, device_info=devInfo)
comm = GVComm(device_info=devInfo, transport=mqtt, protocol=proto)

current_mode = "ON"

###############################################show##################
#
#################################################################
class DemoThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.signal = False
        self.colors = {'Aqua':'00FFFF','Blue':'0000FF','BlueViolet':'8300FE','Chartreuse':'7FFF00','CornflowerBlue':'6495ED','Cornsilk':'FFF8DC','Crimson':'FF0010','Cyan':'00FFFF','DarkBlue':'00008B','DarkCyan':'008B8B','DarkGoldenRod':'B8860B','DarkGreen':'006400','DarkMagenta':'AB008B','DarkOrange':'FF4701','DarkOrchid':'9932CC','DarkRed':'8B0000','DarkSlateBlue':'483D8B','DarkTurquoise':'00CED1','DarkViolet':'9400D3','DeepPink':'FF1493','DeepSkyBlue':'00BFFF','DodgerBlue':'1E90FF','FireBrick':'B22222','ForestGreen':'228B22','Fuchsia':'FF00FF','Gold':'FFD700','GoldenRod':'DAA520','Green':'008000','GreenYellow':'ADFF2F','HotPink':'F501FF','Indigo':'4B0082','LawnGreen':'7CFC00','LemonChiffon':'FFFACD','LightSeaGreen':'20B2AA','LightSkyBlue':'87CEFA','Lime':'00FF00','LimeGreen':'32CD32','Magenta':'FF00FF','MediumAquaMarine':'66CDAA','MediumBlue':'0000CD','MediumPurple':'9370DB','MediumSeaGreen':'3CB371','Olive':'808000','OliveDrab':'6B8E23','Orange':'FE2400','OrangeRed':'FF1100','Orchid':'D700FE','Purple':'AE00FF','Red':'FF0000','Yellow':'FF5E00'}        
        self.k = list(self.colors.keys())
        self.counter = 0;
        self.max_counter = len(self.colors) 
        self.wait = 0.05

    def run(self):
        while True:
            if self.signal:
                self.show()
            elif current_mode == "OFF":
                clear()
            
    def on(self):
        print("DemoThread.ON")
        self.signal = True

    def off(self):
        print("DemoThread.OFF")
        self.signal = False
    
    def show(self):               
        if self.counter >= self.max_counter:
            self.counter = 0
            
        ctxt = self.k[self.counter]
        clear()
        
        # STEP 1
        lcd[0].show(ctxt)
        sleep(self.wait)
        
        # STEP 2
        lcd[0].show("%s\n     %s" %(ctxt,ctxt))
        sleep(self.wait)
        
        # STEP 3
        cluster.show(ctxt, "demo")
        sleep(self.wait)
        
        # STEP 4
        lcd[1].show(ctxt)
        sleep(self.wait)  
        
        # STEP 5
        lcd[1].show("%s\n     %s" %(ctxt,ctxt))        
        sleep(self.wait)
        
        # STEP 6      
        rgb.show(self.colors[ctxt])
        sleep(0.1)
        rgb.clear()
        sleep(0.1)
        rgb.show(self.colors[ctxt])
        sleep(0.1)
        rgb.clear()
        sleep(0.1)
        rgb.show(self.colors[ctxt])
        sleep(1)
        
        self.counter += 1;

#################################################################
#
#################################################################
class HandleDevice(object):
    def __init__(self):
        self.mode = ""

    def __call__(self, payload):
        try:            
            global current_mode, th
            
            data = json.loads(payload.decode("utf-8"))
            current_mode = data.get("value", "OFF").upper() # ON, OFF, DEMO
            
            if current_mode != "DEMO" and self.mode != current_mode:
                self.mode = current_mode
                print("SET DEMO MODE: OFF")                
                demo.off()
                sleep(2)
                lcd[1].show("Green Vulcano\n    Multidisplay")
                
            while current_mode == "DEMO" and self.mode != current_mode:
                self.mode = current_mode
                print("SET DEMO MODE: ON")        
                demo.on()

        except Exception as e:
            print("__call__ exception in HandleDevice")
            print("Exception: %s. Message %s" %(e.args[0], payload.decode("utf-8")))

#################################################################
#
#################################################################
class Handle7Segment(object):
    def __init__(self, display):
        if display < 1 or display > len(all_segments):
            raise Exception('Unknown display')
        self.display = display

    def __call__(self, payload):
        try:
            data = json.loads(payload.decode("utf-8"))        
            value = data["value"]
            
            if current_mode == "ON":
                all_segments[self.display - 1].show(str(value))
                
        except Exception as e:
            print("__call__ exception in Handle7Segment")
            print("Exception: %s. Message %s" %(e.args[0], payload.decode("utf-8")))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print("Error on getData: %s" %str(e))

#################################################################
#
#################################################################
class HandleLCD(object):
    def __init__(self, display):
        self.display = display    

    def __call__(self, payload):
        try:
            data = json.loads(payload.decode("utf-8"))
            value  = data["value"]
            
            if current_mode == "ON":
                lcd[self.display - 1].show(value)
        except Exception as e:
            print("__call__ exception in HandleLCD")
            print("Exception: %s. Message %s" %(e.args[0], payload.decode("utf-8")))

#################################################################
#
#################################################################
class HandleLedRGB(object):
    def __init__(self):
        pass

    def __call__(self, payload):
        try:
            data = json.loads(payload.decode("utf-8"))
            value   = data.get("value", "off")
            type_ = data.get("type", "hex")            

            if value == "":
                value = "off"

            if type_ == "":
                type_ = "hex"

            if current_mode == "ON":
                rgb.show(value, type_)

        except Exception as e:
            print("__call__ exception in HandleLedRGB")
            print("Exception: %s. Message %s" %(e.args[0], payload.decode("utf-8")))

#################################################################
#
#################################################################
def setup():
    comm.add_device(callback=HandleDevice())
    comm.add_actuator(id_="ACD00401", name="Green Display", type_="display", callback=HandleLCD(1))
    comm.add_actuator(id_="ACD00402", name="Blue Display", type_="display", callback=HandleLCD(2))
    comm.add_actuator(id_="ACD00403", name="Seven Segment 1", type_="display", callback=Handle7Segment(1))
    comm.add_actuator(id_="ACD00404", name="Seven Segment 2", type_="display", callback=Handle7Segment(2))
    comm.add_actuator(id_="ACD00405", name="Seven Segment 3", type_="display", callback=Handle7Segment(3))
    comm.add_actuator(id_="ACD00406", name="Seven Segment 4", type_="display", callback=Handle7Segment(4))
    comm.add_actuator(id_="ACD00407", name="Seven Segment Collection", type_="display", callback=Handle7Segment(5))
    comm.add_actuator(id_="ACD00408", name="Led RGB", type_ ="led", callback=HandleLedRGB())

#################################################################
#
#################################################################
def clear():
    # this ensures a clean exit
    for s in all_segments:
        s.clear()
    
    for l in lcd:
        l.clear()
    
    rgb.clear()

#################################################################
#
#################################################################
if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BOARD)

        seg1 = Led7Segment("D7SEG_1", cfg["segment1"], charset)
        seg2 = Led7Segment("D7SEG_2", cfg["segment2"], charset)
        seg3 = Led7Segment("D7SEG_3", cfg["segment3"], charset)
        seg4 = Led7Segment("D7SEG_4", cfg["segment4"], charset)
        cluster = Led7SegmentCluster(seg1, seg2, seg3, seg4)
        all_segments = [seg1, seg2, seg3, seg4, cluster]

        lcd = []
        lcd.append(LiquidCrystal("LCD_TOP", cfg["lcd_top"]))
        lcd.append(LiquidCrystal("LCD_BOTTOM", cfg["lcd_bottom"]))

        rgb = LedRgb("rgb1", cfg["rgb_led"], colorset)

        setup()
        
        demo = DemoThread()
        demo.start()

        lcd[0].show("Device\n    Ready!")

        lcd[1].show("Green Vulcano\n    Multidisplay")

        while True:
            comm.poll()
            sleep(0.05)
            
    except KeyboardInterrupt:  
        print("KeyboardInterrupt")

    except Exception as e:
        print("Exception: %s" %e.args[0])
      
    finally:  
        clear()

        comm.shutdown()
        GPIO.cleanup()
        print("Cleanup Done.")