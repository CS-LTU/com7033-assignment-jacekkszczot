from flask import Flask, render_template

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
