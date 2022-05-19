import serial
import serial.tools.list_ports 

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
            tmp = serial.Serial(x.device)
            mode = tmp.readline().decode().split(',')[0]
            if mode == self.typeof_mc:
                port = x.device 
            tmp.close()
        
        self.ser = serial.Serial(port)

    def get_p(self):
        if self.typeof_mc != 'P':
            return 'Error'

        pressures = self.ser.readline().decode().strip().split(',')

        return pressures
    
    def change_valve(self, valve):

        if valve == 'valve1':
            ser.write('A'.encode())
        elif valve == 'valve2':
            ser.write('B'.encode())
        elif valve == 'valve3':  
            ser.write('C'.encode())
        elif valve == 'valve4':
            ser.write('D'.encode())
        elif valve == 'valve5':
            ser.write('E'.encode())
        elif valve == 'valve6':
            ser.write('F'.encode())