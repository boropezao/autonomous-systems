from flask import Flask, jsonify, request, make_response
import numpy as np
from preprocessing import preprocess_input, inverse_result
from tensorflow import keras

app = Flask(__name__)

@app.route("/sensor", methods=["GET"])
def sensor_data():

    data = {
        "mpu": {
            "x":0.23,
            "y":0.09,
            "z":1.02,
        },
        "bmp": {
            "temperature": 21.5,
            "pressure": 123,
            "altitute": 12344,
        }
    }

    return jsonify(data), 200, {'Access-Control-Allow-Origin':'*'}


@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
        
        if request.method == "OPTIONS":
            # This will handle the preflight request
            print("Here")
            response =make_response('Response')
            headers = response.headers
            headers["Access-Control-Allow-Origin"] = "*"
            headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            return response

        elif request.method == "POST":
    
            data = request.json

            if(data):
                preprocessed = preprocess_input(data)
                print(preprocessed)
                loaded_model = keras.models.load_model("my_model.keras")
                prediction_result = loaded_model.predict(preprocessed)
                print(prediction_result)
                sale_price = inverse_result(prediction_result)
                print(sale_price)
                sale_price = sale_price[0][0]
            
            response = {
                "prediction": str(sale_price),
            }
            
            return jsonify(response), 200, {'Access-Control-Allow-Origin':'*'}


if __name__ == '__main__':
    app.run(debug=True)