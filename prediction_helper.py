import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Path to the save model and its components
MODEL_PATH = 'artifacts/model_data.joblib'

# Load the model and its components
model_data = joblib.load(MODEL_PATH)
model = model_data['model']
scaler = model_data['scaler']
features = model_data['features']
cols_to_scale = model_data['cols_to_scale']

# print("Features:", features)
# print("Type:", type(features))
# print("Scaler was fit on:", scaler.feature_names_in_)


def prepare_df(user_inputs):
    # age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency, delinquency_ratio, credit_utilization_ratio, number_open_accounts, residence_type, loan_purpose, loan_type = **user_inputs

    input_data = {
        'age': user_inputs['age'],
        'income': user_inputs['income'],
        'loan_amount': user_inputs['loan_amount'],
        'loan_to_income': user_inputs['loan_to_income_ratio'],
        'loan_tenure_months': user_inputs['loan_tenure_months'],
        'avg_dpd_per_delinquency': user_inputs['avg_dpd_per_delinquency'],
        'delinquency_ratio': user_inputs['delinquency_ratio'],
        'credit_utilization_ratio': user_inputs['credit_utilization_ratio'],
        'number_of_open_accounts': user_inputs['num_open_accounts'],
        'residence_type_Owned': 1 if user_inputs['residence_type'] == 'Owned' else 0,
        'residence_type_Rented': 1 if user_inputs['residence_type'] == 'Rented' else 0,
        'loan_purpose_Education': 1 if user_inputs['loan_purpose'] == 'Education' else 0,
        'loan_purpose_Home': 1 if user_inputs['loan_purpose'] == 'Home' else 0,
        'loan_purpose_Personal': 1 if user_inputs['loan_purpose'] == 'Personal' else 0,
        'loan_type_Unsecured': 1 if user_inputs['loan_type'] == 'Unsecured' else 0,
        
        # add additional fields
        'number_of_dependants': 1, # Dummy value
        'years_at_current_address': 1, # Dummy value
        'years_at_current_address': 1, # Dummy value
        'sanction_amount': 1, # Dummy value
        'bank_balance_at_application': 1, # Dummy value
        'number_of_closed_accounts': 1, # Dummy value
        'enquiry_count': 1, # Dummy value
        'bank_balance_at_application': 1, # Dummy value
        'gst': 1, # Dummy value
        'net_disbursement': 1, # Dummy value
        'principal_outstanding': 1, # Dummy value
        'processing_fee': 1, # Dummy value
    }
    
    print(f'input data : {input_data}')
    
    df = pd.DataFrame([input_data])
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    
    df = df[features]
    
    return df

def calculate_credit_score(input_df, base_score = 300, scale_length=600):
    x = np.dot(input_df.values, model.coef_.T) + model.intercept_
    
    default_probability = 1 / (1+np.exp(-x))
    non_default_probability = 1 - default_probability
    
    credit_score = base_score + non_default_probability.flatten()[0] * scale_length
    
    # Determine the rating category based on the credit score
    
    rating = get_rating(credit_score)
    
    return default_probability.flatten()[0], int(credit_score), rating

def get_rating(score):
    if 300 <= score < 500:
        return 'Poor'
    elif 500 <= score < 650:
        return 'Average'
    elif 650 <= score < 750:
        return 'Good'
    elif 750 <= score <= 900:
        return 'Excellent'
    else:
        return 'Undefined'

def predict(user_inputs):
    input_df = prepare_df(user_inputs)
    
    (probability, credit_score, rating) = calculate_credit_score(input_df)
    
    return (probability, credit_score, rating)