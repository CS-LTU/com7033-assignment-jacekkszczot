def calculate_stroke_risk(patient_data):
    risk_score = 0
    
    # Age risk
    age = float(patient_data['age'])
    if age > 60:
        risk_score += 0.3
    elif age > 40:
        risk_score += 0.2
        
    # Hypertension risk
    if patient_data['hypertension'] == 1:
        risk_score += 0.2
        
    # Glucose level risk
    glucose = float(patient_data['avg_glucose_level'])
    if glucose > 200:
        risk_score += 0.2
    elif glucose > 140:
        risk_score += 0.1
        
    # BMI risk
    bmi = float(patient_data['bmi'])
    if bmi > 30:
        risk_score += 0.1
        
    # Smoking risk
    if patient_data['smoking_status'] == 'smokes':
        risk_score += 0.1
        
    return min(risk_score, 1.0)  
