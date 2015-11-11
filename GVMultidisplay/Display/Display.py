from abc import ABCMeta, abstractmethod

class Display(metaclass=ABCMeta):
    @abstractmethod
    def show(self, text, opt=None):
        pass
    
    @abstractmethod
    def getText(self):
        pass
    
    @abstractmethod
    def clear(self):
        pass