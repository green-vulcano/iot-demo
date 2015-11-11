from Display import Display
from time import sleep

SLEEP_TIME = 0.15 # seconds 0.15

#######################################################
#
####################################################### 
def rotate(x, y=1):
    if len(x) == 0:
        return x
    
    y = y % len(x) # Normalize y, using modulo - even works for negative y
   
    return x[y:] + x[:y]

#######################################################
#
#######################################################  
class Led7SegmentCluster(Display):
    
    ###################################################
    #
    ###################################################
    def __init__(self, *displays):
        self._displays = [] # lista di display a 7 segmenti
        
        for d in displays:
            self._displays.append(d)
    
    ###################################################
    #
    ###################################################
    def show(self, text, opt=None):
        num = len(self._displays)        
        text = ((num-1) * " ") + text

        # while(True):
        #     for c in range(len(text[0:num])):
        #         self._displays[c].show(text[c])
        #     text = rotate(text)
        #     sleep(0.5)

        for i in range(len(text)-num+1):
            for c in range(len(text[0:num])):
                self._displays[c].show(text[c])
            text = rotate(text)

            if opt != None and str(opt).upper() == "DEMO":
                sleep(SLEEP_TIME)
    
    ###################################################
    #
    ###################################################            
    def getText(self):
        self.text = ""
        
        for d in self._displays:
            self.text += d.getText()
            
        return self.text            
    
    ###################################################
    #
    ###################################################
    def clear(self):
        for d in self._displays:
            d.show(" ")

#######################################################
#
#######################################################      
if __name__ == '__main__':
    text = [1,2,3,4,5,6,7,8,9]
    
    for i in range(100):
        print(text)
        text = rotate(text)   
        sleep(0.25)
    
    
