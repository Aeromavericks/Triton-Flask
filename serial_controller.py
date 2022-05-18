import serial
import serial.tools.list_ports 

class Controller():
    def __init__(self, typeof_mc):
        if typeof_mc.lower() == 'pressure':
            self.typeof_mc = 'P'
        
        else:
            self.typeof_mc = 'V'
        
        self.ser = None

    def connect(self):
        ports = list(serial.tools.list_ports.comports())

        maple_ports = []

        for x in ports:
            if 'Maple' in x.description:
                maple.ports.append(x)

        port = ''

        for x in maple_ports:
            tmp = serial.Serial(x.device)
            mode = tmp.readline().decode().split(',')[0]
            if mode == self.typeof_mc:
                port = x.device 
            tmp.close()

        
        self.ser = serial.Serial(port)

    def get_p(self):

        pressures = self.ser.readline().decode().split(',')

        return pressures