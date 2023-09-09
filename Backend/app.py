import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl","rb"))

@app.route("/predict" , methods = ["GET"])
def predict():
    if request.is_json:
        json_data = request.json
        data = pd.DataFrame(json_data, index=[0])
        query_df = data[['DIM( Days In Milk)','Avg(7 days). Daily MY( L )', 'Kg. milk 305 ( Kg )', 'Fat (%)' , 'SNF (%)', 'Density ( Kg/ m3','Protein (%)','Conductivity (mS/cm)','pH','Freezing point (⁰C)','Salt (%)','Lactose (%)']]
        prediction = model.predict(query_df)
        return jsonify({"Prediction" : list(prediction.astype(str))})
    else:
        return jsonify({"error": "Request is not in JSON format"})

@app.route("/predict/csv" , methods = ["GET"])
def predict_csv():
    #assume csv_file is the file name in the frontend, change it necessarily
    if 'csv_file' not in request.files:
        return "No file part"

    file = request.files['csv_file']

    if file.filename == '':
        return "No selected file"
    
    if file:
        try:
            data = pd.read_excel(file)
            query_df = data[['DIM( Days In Milk)','Avg(7 days). Daily MY( L )', 'Kg. milk 305 ( Kg )', 'Fat (%)' , 'SNF (%)', 'Density ( Kg/ m3','Protein (%)','Conductivity (mS/cm)','pH','Freezing point (⁰C)','Salt (%)','Lactose (%)']]
            index_df = data['Sample No']
            prediction = model.predict(query_df)

            return jsonify({"Sample No" : list(index_df.astype(str)),"Prediction" : list(prediction.astype(str))})
        
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

if __name__ == "__main__" :
    app.run(debug=True)