from flask import Flask, request, jsonify
import pandas as pd
from pypmml import Model

app = Flask(__name__)

# Leitura do arquivo CSV
dataframe = pd.read_csv('diabetes_prediction_dataset_number.csv')

# Obtenha os valores mínimos e máximos de cada coluna
minimos = dataframe.min()
maximos = dataframe.max()

print(minimos)
print(maximos)

@app.route('/', methods=['POST'])
def pmmlPredictor():
   
    json_data = request.get_json()
    print("Cliente requisitado")

    
    gender = (float(json_data['gender']) - minimos['gender']) / (maximos['gender'] - minimos['gender'])
    age = (float(json_data['age']) - minimos['age']) / (maximos['age'] - minimos['age'])
    hypertension = (float(json_data['hypertension']) - minimos['hypertension']) / (maximos['hypertension'] - minimos['hypertension'])
    heart_disease = (float(json_data['heart_disease']) - minimos['heart_disease']) / (maximos['heart_disease'] - minimos['heart_disease'])
    smoking_history = (float(json_data['smoking_history']) - minimos['smoking_history']) / (maximos['smoking_history'] - minimos['smoking_history'])
    blood_glucose_level = (float(json_data['blood_glucose_level']) - minimos['blood_glucose_level']) / (maximos['blood_glucose_level'] - minimos['blood_glucose_level'])
    bmi = (float(json_data['bmi']) - minimos['bmi']) / (maximos['bmi'] - minimos['bmi'])
    if 'HbA1c_level' in json_data:
        HbA1c_level = (float(json_data['HbA1c_level']) - minimos['HbA1c_level']) / (maximos['HbA1c_level'] - minimos['HbA1c_level'])
        pmml_file = './model.pmml' #com Hba1c
    else:
        HbA1c_level = None
        pmml_file = './modelSem.pmml'

  
    data = {
        'gender': gender,
        'age': age,
        'hypertension': hypertension,
        'heart_disease': heart_disease,
        'smoking_history': smoking_history,
        'bmi': bmi,
        'blood_glucose_level': blood_glucose_level,
    }

    if HbA1c_level is not None:
        data['HbA1c_level'] = HbA1c_level
        
        

    model = Model.fromFile(pmml_file)
    prediction = model.predict(data)
    predictionResult = str(prediction)  

   
    return jsonify({'result': predictionResult})

if __name__ == '__main__':
    app.run(debug=True)
