import serial
import serial.tools.list_ports 
import numpy as np
import time


class Controller():
    def __init__(self, typeof_mc): 
        if typeof_mc.lower() == 'pressure': 
            self.typeof_mc = 'P'
            self.filename = str(time.time())
        
        else:
            self.typeof_mc = 'V' 
            self.valve1state = False 
            self.valve2state = False
            self.valve3state = False
            self.valve4state = False
            self.valve5state = False
            self.valve6state = False
        
        self.ser = None
        
    def connect(self):
        ports = list(serial.tools.list_ports.comports())

        maple_ports = []

        for x in ports:
            if 'Maple' in x.description:
                maple_ports.append(x)

        port = ''

        for x in maple_ports:
            tmp = serial.Serial(x.device)
            tmp.reset_input_buffer()
            mode = ''
            while len(mode) != 1:
                mode = tmp.readline().decode().split(',')[0]
                print(mode)
            if mode == self.typeof_mc:
                port = x.device 
            tmp.close()
        
        self.ser = serial.Serial(port)

    def get_p(self): 
        if self.typeof_mc != 'P':
            return 'Error'

        if self.ser != None:
            pressures = self.ser.readline().decode().strip().split(',')
        else:
            pressures = ['P','0','0','0','0','0','0','0','0','0','0']
            print("Pressure mc not connected")

        logfile = open("data/"+self.filename, 'a+') 
        for x in pressures:
            logfile.write(x+', ')

        logfile.write('\n')
        logfile.close()

        return pressures
    
    def get_p_avg(self):

        pressures = []
       
        for i in range(10):
            pressures.append(self.get_p())
            time.delay(0.1)
            
        pressures = np.array(pressures)
        avg = np.average(pressures, axis=0)

        return avg 
    
    def change_valve(self, valve):

        if valve == 'valve1':
            self.ser.write('A'.encode())
            print("Reached Here")
        elif valve == 'valve2':
            self.ser.write('B'.encode())
        elif valve == 'valve3':  
            self.ser.write('C'.encode())
        elif valve == 'valve4':
            self.ser.write('D'.encode())
        elif valve == 'valve5':
            self.ser.write('E'.encode())
        elif valve == 'valve6':
            self.ser.write('F'.encode())