from flask import Flask, request, jsonify
from pypmml import Model

app = Flask(__name__)

@app.route('/', methods=['POST'])
def pmmlPredictor():
    # Obtenha o JSON enviado pelo aplicativo React
    json_data = request.get_json()
    print("Cliente requisitado")

    # Obtenha os dados do JSON e converta-os para os tipos de dados corretos
    gender = float(json_data['gender'])
    age = float(json_data['age'])
    hypertension = float(json_data['hypertension'])
    heart_disease = float(json_data['heart_disease'])
    smoking_history = float(json_data['smoking_history'])
    blood_glucose_level = float(json_data['blood_glucose_level']) 
    bmi = float(json_data['bmi'])
    if 'HbA1c_level' in json_data:
        HbA1c_level = float(json_data['HbA1c_level'])
        pmml_file = './model.pmml' #com Hba1c
        
    else:
        HbA1c_level = None
        pmml_file = './modelSem.pmml'

    # Crie um dicionário de dados para passar para o modelo
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
        
    # Faça a previsão do modelo
    model = Model.fromFile(pmml_file)
    prediction = model.predict(data)
    predictionResult = str(prediction)  # convert the prediction to a string


    # Retorne a previsão como um JSON para o aplicativo React
    response_data = {"prediction": predictionResult}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
