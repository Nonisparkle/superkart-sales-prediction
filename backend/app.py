
# Import necessary libraries
import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app with a name
superkart_api = Flask("SuperKart")

# Load the trained model pipeline (preprocessing + estimator)
model = joblib.load("superkart_model.joblib")

# The feature order and names must match the training pipeline
FEATURE_COLUMNS = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years",
    "Product_Type_Category",
]

@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart System"

@superkart_api.post('/v1/predict')
def predict_sales():
    try:
        data = request.get_json(force=True)
        missing = [column for column in FEATURE_COLUMNS if column not in data]
        if missing:
            return jsonify({"error": "Missing required fields: " + ", ".join(missing)}), 400
        sample = {column: data[column] for column in FEATURE_COLUMNS}
        input_data = pd.DataFrame([sample], columns=FEATURE_COLUMNS)
        prediction = float(model.predict(input_data)[0])
        return jsonify({"Sales": round(prediction, 2)})
    except Exception as error:
        return jsonify({"error": str(error)}), 400

@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Upload a CSV file using the 'file' field."}), 400
        input_data = pd.read_csv(request.files['file'])
        missing = [column for column in FEATURE_COLUMNS if column not in input_data.columns]
        if missing:
            return jsonify({"error": "Missing required columns: " + ", ".join(missing)}), 400
        input_data = input_data[FEATURE_COLUMNS]
        predictions = model.predict(input_data).astype(float).tolist()
        output_dict = {str(index): round(prediction, 2) for index, prediction in enumerate(predictions)}
        return jsonify(output_dict)
    except Exception as error:
        return jsonify({"error": str(error)}), 400

if __name__ == '__main__':
    superkart_api.run(host='0.0.0.0', port=7860)
