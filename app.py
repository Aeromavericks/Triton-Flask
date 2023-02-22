from flask import Flask, render_template, stream_with_context, Response
import serial_controller
import time,json
from datetime import datetime
from typing import Iterator

app = Flask(__name__) 
#
pressure_controller = serial_controller.Controller('pressure') # create pressure controller
valve_controller = serial_controller.Controller('valve') # create valve controller

@app.route('/') # main page
def index(): 
    return render_template('index.html') # render index.html

def pressure_data_source() -> Iterator[str]: # function to send data to client
    while True:
        pressures = pressure_controller.get_p() # get pressure data from serial

        json_data_chart = json.dumps({ # format data for chart.js
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # time
            "value1": int(pressures[1]), # pressure 1
            "value2": int(pressures[2]), # pressure 2
            })

        yield f"data:{json_data_chart}\n\n" # send data to client
            

@app.route('/valve_toggle/<valvename>') # route to toggle valve
def valve_toggle(valvename):
    valve_controller.change_valve(valvename)
    return {valvename:'changed'}

@app.route("/data") # route to send data to client
def chart_data() -> Response: # function to send data to client
    response = Response(stream_with_context(pressure_data_source()), mimetype="text/event-stream") # send data to client
    response.headers["Cache-Control"] = "no-cache" # disable caching
    response.headers["X-Accel-Buffering"] = "no" # disable buffering
    return response 

if __name__ == '__main__':
    pressure_controller.connect() # connect to serial port
    valve_controller.connect() # connect to serial port
    
    app.run(host='0.0.0.0', debug=True, threaded=True) # run app