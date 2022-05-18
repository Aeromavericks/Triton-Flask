from flask import Flask, render_template
import serial_controller

app = Flask(__name__)
pressure_controller = serial_controller.Controller('pressure')

@app.route('/')
def index():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0" )
    pressure_controller.connect()