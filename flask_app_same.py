from flask import Flask, request
import numpy as np
import pickle
import pandas as pd
import flasgger
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

# Load the model
pickle_in = open("model.pkl", "rb")
classifier = pickle.load(pickle_in)

@app.route('/')
def welcome():
    return "Welcome to the Random Forest Classifier API!"

@app.route('/predict', methods=["GET"])
def predict_note_authentication():
    """Authenticate the Bank Note 
    This uses docstrings for specifications.
    ---
    parameters:  
      - name: variance
        in: query
        type: number
        required: true
      - name: skewness
        in: query
        type: number
        required: true
      - name: curtosis
        in: query
        type: number
        required: true
      - name: entropy
        in: query
        type: number
        required: true
    responses:
        200:
            description: The output values
    """
    try:
        variance = float(request.args.get("variance"))
        skewness = float(request.args.get("skewness"))
        curtosis = float(request.args.get("curtosis"))
        entropy = float(request.args.get("entropy"))

        # Perform prediction
        prediction = classifier.predict([[variance, skewness, curtosis, entropy]])
        return "Prediction result: " + str(prediction)
    
    except Exception as e:
        return str(e)

@app.route('/predict_file', methods=["POST"])
def predict_note_file():
    """Authenticate the Bank Note using a file
    This uses docstrings for specifications.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
      
    responses:
        200:
            description: The output values
    """
    try:
        # Read the uploaded CSV file
        df_test = pd.read_csv(request.files.get("file"))
        
        # Checking DataFrame has the correct number of columns or not
        if df_test.shape[1] != 4:
            return "Error: The input file must contain exactly 4 features."

        # Perform prediction
        prediction = classifier.predict(df_test)
        return str(list(prediction))
    
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)