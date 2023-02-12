from flask import Flask, render_template, request, stream_with_context, Response
import serial_controller
import threading, time,json
from datetime import datetime
from typing import Iterator

pressure_controller = serial_controller.Controller('pressure')

valve_controller = serial_controller.Controller('valve')

@app.route('/')
def index():
    return render_template('index.html')

def pressure_data_source() -> Iterator[str]:
    while True:
        pressures = pressure_controller.get_p()

        json_data_chart = json.dumps({
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "value1": int(pressures[1]),
            "value2": int(pressures[2]),
            })

        yield f"data:{json_data_chart}\n\n"
            

@app.route('/valve_toggle/<valvename>')
def valve_toggle(valvename):
    valve_controller.change_valve(valvename)
    return {valvename:'changed'}

@app.route("/data")
def chart_data() -> Response:
    response = Response(stream_with_context(pressure_data_source()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

if __name__ == '__main__':
    pressure_controller.connect()
    valve_controller.connect()
    
    app.run(host='0.0.0.0', debug=True,threaded=True)