from flask import Flask, render_template
import serial_controller
import serial_controllerStub
import sys, time, requests
from threading import Thread, Lock

app = Flask(__name__) 

pressure_controller = None
valve_controller = None
last_pressure = {"P1": 0, "P2": 0}
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
    valve_controller.change_valve(valvename)
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
        print(tmp)
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
