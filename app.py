from flask import Flask, render_template, redirect, request
from clientReader import *
from pyModbusTCP.client import ModbusClient
import Adafruit_DHT

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route("/rotate_90")
def rotate_90():
    angle = 90
    client2 = ModbusClient(host='localhost', port=1502, unit_id=1, timeout=60.0, debug=False, auto_open=True, auto_close=False)
    
    if client2.write_single_register(0, angle):
        register_move_servo(0, 1)
        return redirect("/")
    else:
        home_page()

@app.route("/rotate_180")
def rotate_180():
    angle = 180
    client2 = ModbusClient(host='localhost', port=1502, unit_id=1, timeout=60.0, debug=False, auto_open=True, auto_close=False)
    
    if client2.write_single_register(0, angle):
        register_move_servo(0, 1)
        return redirect("/")
    else:
        home_page()

@app.route("/rotate_90_180")
def rotate_90_180():
    angle1, angle2 = 90, 180
    client2 = ModbusClient(host='localhost', port=1502, unit_id=1, timeout=60.0, debug=False, auto_open=True, auto_close=False)
    
    angles = [angle1, angle2]
    if client2.write_multiple_registers(0, angles):
        register_move_servo(0, 2)
        return redirect("/")
    else:
        home_page()
    

@app.route("/step_motor")
def step_motor_page():
    return render_template('cmp_form.html')

@app.route('/move_step_motor', methods = ['POST'])
def data():
    if request.method == 'POST':
        data = request.form
        parameters = [ int(x) for x in [ data['time'], data['angleOfRotation'], data['direction'] ] ]
        print(parameters)
        # for elem in data:
        #     #print(elem)
        #     print(f"key is {elem} with value {data[elem]}")

        client2 = ModbusClient(host='localhost', port=1502, unit_id=1, timeout=60.0, debug=False, auto_open=True, auto_close=False)

        if client2.write_multiple_registers(0, parameters):
            print('true')
            registers_move_step(0, len(parameters))

        return redirect("/")

'''
    form_time = request.form["time"]
    form_angle = request.form["angleOfRotation"]
    form_direction = request.form["direction"]
    data = [int(form_time), int(form_angle), int(form_direction)]
    return data
    '''

def rotate_step():
    client2 = ModbusClient(host='localhost', port=1502, unit_id=1, timeout=60.0, debug=False, auto_open=True, auto_close=False)

    parameters = data()
    if client2.write_multiple_registers(0, parameters):
        registers_move_step(0, len(parameters))
    else: 
        home_page()


@app.route("/show_par")
def show_par():
    # prendere parametri
    sensor = 11
    gpio = 4
    um, temp = Adafruit_DHT.read_retry(sensor, gpio)
    print(um, temp)
    parameters = [int(um), int(temp)]


    #um, temp = 4, 69
    # scriverli tramite modbus
    client2 = ModbusClient(host='localhost', port=1502, unit_id=1, timeout=60.0, debug=False, auto_open=True, auto_close=False)

    # leggere tramite modbus, ottieni temp e um, chiama give data
    if um is not None and temp is not None:
        tmp = client2.write_multiple_registers(0, parameters)
        if tmp:
            values_list = give_data(0, 2)
            return render_template('show_par.html', temper=values_list[1], umid=values_list[0])
    else:
        return render_template('show_par.html', temper=0, umid=0)
    
    