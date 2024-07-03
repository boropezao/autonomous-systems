from flask import Flask, jsonify
import sensorreader

app = Flask(__name__)

sensor = sensorreader.SensorReader()

@app.route("/sensor", methods=["GET"])
def sensor_data():

    ax, ay, az, temp, pres, alt = sensor.read_sensors()
    
    x = round((ax * 3.0 + 1.0))
    y = round((ay * 3.0 + 1.0))
    z = round((az * 3.0 + 1.0))
    
    data = {
        "mpu": {
            "x": x,
            "y": y,
            "z": z
            },
        "bmp": {
            "temperature": temp,
            "presure": pres,
            "altitute": alt
            }
        }

    return jsonify(data), 200, {'Access-Control-Allow-Origin':'*'}

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

