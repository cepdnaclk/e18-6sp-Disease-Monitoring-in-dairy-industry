import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app

model = pickle.load(open("model.pkl","rb"))

@app.route("/predict" , methods = ["POST"])
def predict():
    if request.is_json:
        json_data = request.json
        data = pd.DataFrame(json_data, index=[0])
        query_df = data[['DIM( Days In Milk)','Avg(7 days). Daily MY( L )', 'Kg. milk 305 ( Kg )', 'Fat (%)' , 'SNF (%)', 'Density ( Kg/ m3','Protein (%)','Conductivity (mS/cm)','pH','Freezing point (⁰C)','Salt (%)','Lactose (%)']]
        prediction = model.predict(query_df)
        return jsonify({"Prediction" : list(prediction.astype(str))}),200
    else:
        return jsonify({"error": "Request is not in JSON format"}),500

@app.route("/predict/csv" , methods = ["POST"])
def predict_csv():
    #assume csv_file is the file name in the frontend, change it necessarily
    if 'csv_file' not in request.files:
        return "No file part", 400

    file = request.files['csv_file']

    if file.filename == '':
        return "No selected file",400
    
    if file:
        try:
            data = pd.read_excel(file)
            query_df = data[['DIM( Days In Milk)','Avg(7 days). Daily MY( L )', 'Kg. milk 305 ( Kg )', 'Fat (%)' , 'SNF (%)', 'Density ( Kg/ m3','Protein (%)','Conductivity (mS/cm)','pH','Freezing point (⁰C)','Salt (%)','Lactose (%)']]
            index_df = data['Sample No']
            prediction = model.predict(query_df)

            return jsonify({"Sample No" : list(index_df.astype(str)),"Prediction" : list(prediction.astype(str))}),200
        
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}),500

if __name__ == "__main__" :
    app.run(debug=True)