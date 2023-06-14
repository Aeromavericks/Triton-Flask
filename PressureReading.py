class PressureReading:

    pressure_sensor1 = 0.0
    pressure_sensor2 = 0.0
    pressure_sensor3 = 0.0
    pressure_sensor4 = 0.0
    pressure_sensor5 = 0.0
    pressure_sensor6 = 0.0
    pressure_sensor7 = 0.0
    pressure_sensor8 = 0.0
    pressure_sensor9 = 0.0
    pressure_sensor10 = 0.0

    def __init__(self, pressure_sensor_readings):
        #TODO: Check if valid reading before reading array
        self.pressure_sensor1 = pressure_sensor_readings[0]
        self.pressure_sensor2 = pressure_sensor_readings[1]
        self.pressure_sensor3 = pressure_sensor_readings[2]
        self.pressure_sensor4 = pressure_sensor_readings[3]
        self.pressure_sensor5 = pressure_sensor_readings[4]
        self.pressure_sensor6 = pressure_sensor_readings[5]
        self.pressure_sensor7 = pressure_sensor_readings[6]
        self.pressure_sensor8 = pressure_sensor_readings[7]
        self.pressure_sensor9 = pressure_sensor_readings[8]
        self.pressure_sensor10 = pressure_sensor_readings[9]

    def get_pressure_sensor1(self):
        return float(self.pressure_sensor1)

    def get_pressure_sensor2(self):
        return float(self.pressure_sensor2)

    def get_pressure_sensor3(self):
        return float(self.pressure_sensor3)

    def get_pressure_sensor4(self):
        return float(self.pressure_sensor4)

    def get_pressure_sensor5(self):
        return float(self.pressure_sensor5)

    def get_pressure_sensor6(self):
        return float(self.pressure_sensor6)

    def get_pressure_sensor7(self):
        return float(self.pressure_sensor7)

    def get_pressure_sensor8(self):
        return float(self.pressure_sensor8)

    def get_pressure_sensor9(self):
        return float(self.pressure_sensor9)

    def get_pressure_sensor10(self):
        return float(self.pressure_sensor10)


