def validate_patient_data(data):
    if not 0 <= float(data['age']) <= 120:
        return False, "Age must be between 0 and 120"
    
    if data['gender'] not in ['Male', 'Female', 'Other']:
        return False, "Invalid gender"
    
    if data['hypertension'] not in [0, 1]:
        return False, "Hypertension must be 0 or 1"
    
    if data['ever_married'] not in ['Yes', 'No']:
        return False, "Ever married must be Yes or No"
    
    if data['residence_type'] not in ['Rural', 'Urban']:
        return False, "Residence type must be Rural or Urban"
    
    if not 0 <= float(data['avg_glucose_level']) <= 500:
        return False, "Invalid glucose level"
    
    if not 10 <= float(data['bmi']) <= 50:
        return False, "BMI must be between 10 and 50"
        
    return True, "Data is valid"