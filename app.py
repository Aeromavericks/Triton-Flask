from flask import Flask, render_template
import serial_controller

app = Flask(__name__)
pressure_controller = serial_controller.Controller('pressure')

@app.route('/')
def index():
    print(pressure_controller.get_p())
    return render_template('index.html', value = '100')



if __name__ == '__main__':
    pressure_controller.connect()
    app.run(host='0.0.0.0', debug=True)
    