import joblib
import os
from django.conf import settings
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

MODEL_PATH = os.path.join(settings.BASE_DIR, 'appname', 'model', 'best_model.pkl')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'appname', 'model', 'scaler.pkl')
LABEL_ENCODER_PATH = os.path.join(settings.BASE_DIR, 'appname', 'model', 'label_encoder.pkl')
METADATA_PATH = os.path.join(settings.BASE_DIR, 'appname', 'model', 'feature_metadata.pkl')
TRAINED_DATA_PATH = os.path.join(settings.BASE_DIR, 'appname', 'model', 'trained_data.joblib')

# Load model and preprocessing components
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)
metadata = joblib.load(METADATA_PATH)
numeric_features = metadata['numeric_features']
feature_columns = metadata['feature_columns']
# feature_columns = ['Age', 'GraduateOrNot', 'AnnualIncome', 'FamilyMembers', 'ChronicDiseases', 'FrequentFlyer', 'EverTravelledAbroad', 'Employment_Type_Government_Sector', 'Employment_Type_Private_Sector_or_Self_Employed']
# feature_columns = ['Age', 'GraduateOrNot', 'AnnualIncome', 'FamilyMembers', 'ChronicDiseases', 'FrequentFlyer', 'EverTravelledAbroad', 'Employment Type_Government Sector', 'Employment Type_Private Sector/Self Employed']



def predict_insurance(form_data):
    print(f"Form Data received by predict_insurance: {form_data}")
    print(f"feature_columns in predict_insurance: {feature_columns}") 
    
    try:
        input_data = []
        for col in feature_columns:
            value = form_data.get(col)
            if value is None:
                error_message = f"Error: Missing feature in form: {col}"
                print(error_message)
                return error_message
            
            if col in ['Age', 'FamilyMembers', 'GraduateOrNot', 'ChronicDiseases', 'FrequentFlyer', 'EverTravelledAbroad', 'Employment_Type_Government_Sector', 'Employment_Type_Private_Sector_or_Self_Employed']:
                try:
                    input_data.append(int(value))  
                except ValueError:
                    error_message = f"Error: Invalid value for {col}: {value}"
                    print(error_message)
                    return error_message
            elif col == 'AnnualIncome':
                try:
                    input_data.append(float(value)) 
                except ValueError:
                    error_message = f"Error: Invalid value for {col}: {value}"
                    print(error_message)
                    return error_message
            else:
                input_data.append(value)

        input_df = pd.DataFrame([input_data], columns=feature_columns)
        input_df_scaled = input_df[numeric_features].copy()
        input_df[numeric_features] = scaler.transform(input_df_scaled)

        prediction_proba = model.predict_proba(input_df)
        prediction = model.predict(input_df)
        probability_of_buying = prediction_proba[0][1] * 100
        predicted_class = "Will likely buy" if prediction[0] == 1 else "Will likely not buy"
        result = predicted_class, f"{probability_of_buying:.2f}%"
        print(f"Result from predict_insurance: {result}")
        return result
    except Exception as e:
        error_message = f"Exception in predict_insurance: {e}"
        print(error_message)
        return error_message
    