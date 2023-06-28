from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the pickled model
with open('Server/predict_model_lanslide.pkl', 'rb') as file:
    model = pickle.load(file)

with open('Server/scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)


@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get the input data from the POST request
            input_data = request.get_json()
            del input_data["id"]
            print(input_data)
            print(type(input_data))

            input_row_df = np.array(list(input_data.values())).reshape(1, -1)

            scaled_input_row = scaler.transform(input_row_df)

            # Make the prediction using the loaded model
            prediction = model.predict(scaled_input_row)

            # Return the prediction as a JSON response
            return jsonify({'prediction': prediction[0]})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    else:
        return 'Server is running. Send a POST request to this endpoint to make predictions.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
