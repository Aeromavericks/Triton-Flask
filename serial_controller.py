import serial
import serial.tools.list_ports 
import numpy as np
import time


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

    def connect(self):
        ports = list(serial.tools.list_ports.comports())

        maple_ports = []

        for x in ports:
            if 'Maple' in x.description:
                maple_ports.append(x)

        port = ''

        for x in maple_ports:
            tmp = serial.Serial(x.device) # open serial port
            tmp.reset_input_buffer() # clear buffer
            mode = '' # read mode
            while len(mode) != 1: # wait for mode to be read
                mode = tmp.readline().decode().split(',')[0] # read mode
                print(mode)
            if mode == self.typeof_mc:
                port = x.device 
            tmp.close() # close serial port
        
        self.ser = serial.Serial(port)

    def get_p(self): 
        if self.typeof_mc != 'P':
            return 'Error'

        if self.ser != None: # if serial port is open
            pressures = self.ser.readline().decode().strip().split(',') # read pressure data
        else: # if serial port is not open
            pressures = ['P','0','0','0','0','0','0','0','0','0','0'] # return 0
            print("Pressure mc not connected")

        return pressures # returns list of pressures
    
#    def get_p_avg(self):
 #       pressures = []

  #      for i in range(10):
   #         pressures.append(self.get_p())
    #        time.delay(0.1)

     #   pressures = np.array(pressures)
      #  avg = np.average(pressures, axis=0)

       # return avg 
    
    def change_valve(self, valve):

        if valve == 'valve1':
            self.ser.write('A'.encode())
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