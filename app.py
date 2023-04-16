from flask import Flask, render_template
import serial_controller
import serial_controllerStub
import sys, time, requests
from threading import Thread, Lock

app = Flask(__name__) 

pressure_controller = None
valve_controller = None
last_pressure = {"P1": 0, "P2": 0}
valve_states = {'valve1':0, 'valve2': 0, 'valve3': 0, 'valve4':0, 'valve5':0}
mutex = Lock()

def initializeSerialControllers() -> None:
    global pressure_controller, valve_controller
    pressure_controller = serial_controller.Controller('pressure')
    valve_controller = serial_controller.Controller('valve')

def initializeSerialControllerStubs() -> None:
    global pressure_controller, valve_controller
    pressure_controller = serial_controllerStub.Controller('pressure')
    valve_controller = serial_controllerStub.Controller('valve')

@app.route('/')
def index(): 
    return render_template('index.html')   

@app.route('/valve_toggle/<valvename>')
def valve_toggle(valvename):
    global valve_states
    valve_controller.change_valve(valvename)
    mutex.acquire()
    if valve_states[valvename] == 0:
        valve_states[valvename] = 1
    else :
        valve_states[valvename] = 0
    print(valve_states)
    mutex.release()
    return {valvename:'changed'}

@app.route("/pressure_data")
def pressure_data():
    global last_pressure
    mutex.acquire()
    tmp = last_pressure
    mutex.release()
    return tmp

def worker_thread():
    global last_pressure
    while True:
        pressures = pressure_controller.get_p()
        tmp = {"P1": pressures[1], "P2": pressures[2]}
        #write db part
        url_string = 'http://localhost:8086/write?db=lre'
        mutex.acquire()
        data_string = 'data p1='+str(pressures[1])+',p2='+str(pressures[2])+',valve1='+str(valve_states['valve1'])+',valve2='+str(valve_states['valve2'])+',valve3='+str(valve_states['valve3'])+',valve4='+str(valve_states['valve4'])+',valve5='+str(valve_states['valve5'])
        print(data_string)
        mutex.release()
        r = requests.post(url_string, data=data_string)
        print('added to db')        
        mutex.acquire()
        last_pressure = tmp
        mutex.release()
        time.sleep(0.5)

if __name__ == '__main__':
    
    if len(sys.argv) > 1 and sys.argv[1].upper() == 'DEBUG':
        initializeSerialControllerStubs()
    else:
        initializeSerialControllers()

    pressure_controller.connect()
    valve_controller.connect()
    t = Thread(target = worker_thread)
    t.start()
    app.run(host='0.0.0.0', threaded=True)
