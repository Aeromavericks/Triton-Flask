from flask import Flask, render_template
import serial_controller

app = Flask(__name__)
pressure_controller = serial_controller.Controller('pressure')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
    pressure_controller.connect()