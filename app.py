import re
from flask import Flask, render_template, request, stream_with_context, Response
import serial_controller
from turbo_flask import Turbo
import threading, time, sys, random, webbrowser,json,logging
from datetime import datetime
from typing import Iterator
import filetest

# This is the change I made

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__) 
turbo = Turbo(app)
random.seed()
pressure_controller = serial_controller.Controller('pressure')

valve_controller = serial_controller.Controller('valve')
#values = [600]
sleeptime = 0.1
tList = filetest.SimData()[0]
pList = filetest.SimData()[1]
Len = len(tList)

@app.route('/')
def index():
    return render_template('index.html')
def ip():
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr or ""
    return client_ip
def generate_random_data() -> Iterator[str]:
    """
    Generates random value between 0 and 100
    :return: String containing current timestamp (YYYY-mm-dd HH:MM:SS) and randomly generated data.
    """
    sleepNum = 0.0
    j = 0
    print(Len)
    try:
        logger.info("Client %s connected", ip())
        while True:
            time.sleep(sleeptime)
            i=0
            if j < Len-1:
                pValuefl=float(pList[j])

            
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
            
    except GeneratorExit:
        logger.info("Client %s disconnected", ip())

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