# risk_calc.py
def calculate_stroke_risk(patient_data):
    """Calculate stroke risk based on patient data"""
    risk_score = 0.0
    
    
    # risk elements
    # Age 
    if float(patient_data['age']) > 60:
        risk_score += 0.3
        
    # Hypertension
    if patient_data['hypertension'] == 1:
        risk_score += 0.3
        
    # Glucose level 
    if float(patient_data['avg_glucose_level']) > 200:
        risk_score += 0.2
        
    # Smoking 
    if patient_data.get('smoking_status', '').lower() == 'smokes':
        risk_score += 0.2
        
    return min(risk_score, 1.0)  # Max risk = 100%