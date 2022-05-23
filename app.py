from flask import Flask, render_template, request, stream_with_context, Response
import serial_controller
from turbo_flask import Turbo
import threading, time, sys, random, webbrowser,json,logging
from datetime import datetime
from typing import Iterator

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
turbo = Turbo(app)
random.seed()
#pressure_controller = serial_controller.Controller('pressure')

#valve_controller = serial_controller.Controller('valve')
values = [600]
@app.route('/')
def index():
    return render_template('index.html')

def generate_random_data() -> Iterator[str]:
    """
    Generates random value between 0 and 100
    :return: String containing current timestamp (YYYY-mm-dd HH:MM:SS) and randomly generated data.
    """
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr or ""

    try:
        logger.info("Client %s connected", client_ip)
        while True:
            json_data = json.dumps(
                {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "value": random.randrange(0,1000,1),
                }
            )
            yield f"data:{json_data}\n\n"
            time.sleep(1)
    except GeneratorExit:
        logger.info("Client %s disconnected", client_ip)


#@app.route('/valve_toggle/<valvename>')
#def valve_toggle(valvename):
    #call change valve here
    #valve_controller.change_valve(valvename)
    #return {valvename:'changed'}

@app.route("/chart-data")
def chart_data() -> Response:
    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

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
    
    app.run(host='0.0.0.0', debug=True,threaded=True)
    