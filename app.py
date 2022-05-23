from flask import Flask, render_template
import serial_controller
from turbo_flask import Turbo
import threading, time, sys, random,json

app = Flask(__name__)
turbo = Turbo(app)
#pressure_controller = serial_controller.Controller('pressure')

#valve_controller = serial_controller.Controller('valve')
values = [600]
@app.route('/')
def index():
    legend = 'Random Num'
    return render_template('index.html',legend=legend)


#@app.route('/valve_toggle/<valvename>')
#def valve_toggle(valvename):
    #call change valve here
    #valve_controller.change_valve(valvename)
    #return {valvename:'changed'}

@app.before_first_request
def before_first_request():
    #threading.Thread(target=update_pressure).start()
    threading.Thread(target=update_rand).start()

def update_rand():
    with app.app_context():
        while True:
            time.sleep(0.5)
            print('Update send')
            turbo.push(turbo.replace(render_template('rand.html'),'radial-gauge-1'))
            turbo.push(turbo.replace(render_template('rand2.html'),'radial-gauge-2'))

@app.context_processor
def inject_rand():
    press = random.randrange(0,1000,1)
    pressStr = str(press)
    values.append(press)
    print(press)
    return {'rand1': press}


#def update_pressure():
    #with app.app_context():
        #while True:
            #time.sleep(0.5)
            #print('Update send')
            #turbo.push(turbo.replace(render_template('loadavg.html'), 'pressure'))

#@app.context_processor
#def inject_load():
#    pressures = pressure_controller.get_p()
#    print(pressures)
#    return {'load1': pressures[0], 'load5': pressures[1], 'load15': pressures[2]}

if __name__ == '__main__':
#    pressure_controller.connect()
#    valve_controller.connect()
    
    app.run(host='0.0.0.0', debug=True)
    