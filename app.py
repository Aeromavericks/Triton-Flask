from flask import Flask, render_template, request, stream_with_context, Response
import serial_controller
import threading, time, sys, random, webbrowser,json,logging
from datetime import datetime
from typing import Iterator

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

random.seed()
pressure_controller = serial_controller.Controller('pressure')

valve_controller = serial_controller.Controller('valve')
sleeptime = 0.1


@app.route('/')
def index():
    return render_template('index.html')

def generate_random_data() -> Iterator[str]:
    while True:
        pressures = pressure_controller.get_p()
        json_data_chart = json.dumps(
            {
                "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "value1": int(pressures[1]),
                "value2": int(pressures[2]),
            }
            )
        j=j+1
        yield f"data:{json_data_chart}\n\n"
            

@app.route('/valve_toggle/<valvename>')
def valve_toggle(valvename):
    #call change valve here
    valve_controller.change_valve(valvename)
    return {valvename:'changed'}

@app.route("/data")
def chart_data() -> Response:
    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

if __name__ == '__main__':
    pressure_controller.connect()
    valve_controller.connect()
    
    app.run(host='0.0.0.0', debug=True,threaded=True)