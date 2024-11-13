from flask import Flask, render_template
from risk_calc import calculate_stroke_risk

app = Flask(__name__)
app.secret_key = 'dev'  # change it in a safety key


@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/user_login')
def user_login():
    return render_template('user_login.html')

@app.route('/user_register')
def user_register():
    return render_template('user_register.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/patients_list')
@login_required
def patients_list():
    patient_list = patients.find()
    return render_template('patient_base.html', patients=patient_list)

@app.route('/patient_info/<string:patient_id>')
@login_required
def patient_info(patient_id):
    patient = patients.find_one({'_id': ObjectId(patient_id)})
    if patient:
        return render_template('patient_info.html', patient=patient)
    flash('Patient not found!')
    return redirect(url_for('patients_list'))

@app.route('/add_patient', methods=['POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        patient_data = {
            'gender': request.form['gender'],
            'age': float(request.form['age']),
            'hypertension': int(request.form['hypertension']),
            'avg_glucose_level': float(request.form['avg_glucose_level']),
            'smoking_status': request.form.get('smoking_status', 'Unknown')
        }
        
        # Calculate the risk
        stroke_risk = calculate_stroke_risk(patient_data)
        patient_data['stroke_risk'] = stroke_risk
        
        # Database uodate
        patients.insert_one(patient_data)
        
        return render_template('patient_result.html',
                             stroke_risk=stroke_risk,
                             hypertension=patient_data['hypertension'],
                             age=patient_data['age'],
                             glucose=patient_data['avg_glucose_level'],
                             smoking=patient_data['smoking_status'])

