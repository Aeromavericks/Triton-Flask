from flask import Flask, render_template
import serial_controller
from turbo_flask import Turbo
import threading, time, sys

app = Flask(__name__)
turbo = Turbo(app)
pressure_controller = serial_controller.Controller('pressure')
valve_controller = serial_controller.Controller('valve')

@app.route('/')
def index():
    return render_template('index.html', value = '100')

@app.route('/valve_toggle/<valvename>')
def valve_toggle(valvename):
    #call change valve here
    valve_controller.change_valve(valvename)
    print('Here called '+valvename)
    return {valvename:'changed'}

@app.route('/test')
def test():
    return render_template('test.html')

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_pressure).start()

def update_pressure():
    with app.app_context():
        while True:
            time.sleep(0.5)
            turbo.push(turbo.replace(render_template('loadavg.html'), 'pressure'))

@app.context_processor
def inject_load():
    pressures = pressure_controller.get_p()

    return {'load1': pressures[0], 'load5': pressures[1], 'load15': pressures[2]}

if __name__ == '__main__':
    pressure_controller.connect()
    valve_controller.connect()
    
    app.run(host='0.0.0.0', debug=True)
    