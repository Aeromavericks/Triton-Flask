import random

class Controller():
    def __init__(self, typeof_mc): 
        if typeof_mc.lower() == 'pressure': 
            self.typeof_mc = 'P' 
        
        else:
            self.typeof_mc = 'V' 
            self.valve1state = False 
            self.valve2state = False
            self.valve3state = False
            self.valve4state = False
            self.valve5state = False
            self.valve6state = False
        
        self.ser = None
        self.pressure = 200

    def connect(self):
        self.ser = 'connected'

    def get_p(self): 
        if self.typeof_mc != 'P':
            return 'Error'

        if self.ser != None:
            self.pressure = random.randrange(0, 200)
            pressures = [
                'P',
                self.pressure,
                self.pressure,
                self.pressure,
                self.pressure,
                self.pressure,
                self.pressure,
                self.pressure,
                self.pressure,
                self.pressure,
                self.pressure]

            return pressures

    def change_valve(self, valve):
        pass
    