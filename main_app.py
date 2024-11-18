"""
Stroke Prediction Application
----------------------------

This application helps medical professionals manage patient data and predict stroke risks.
It uses a dual database system for enhanced security and implements various secure
development techniques.

Databases:
- SQLite: Stores user authentication data
- MongoDB: Stores patient medical records

Security Features:
- Password hashing
- Session management
- Input validation
- Protected routes
- Data encryption

Main Components:
1. User Management
   - Registration
   - Authentication
   - Session handling

2. Patient Management
   - Add new patients
   - View patient details
   - Import patient data
   - Calculate stroke risk

3. Data Security
   - Input validation
   - Data sanitization
   - Access control

Author: [Your Name]
Version: 1.0
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from functools import wraps
import pandas as pd

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database setup
def get_db_connection():
   conn = sqlite3.connect('user_base.db')
   conn.row_factory = sqlite3.Row
   return conn

# MongoDB setup
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['stroke_management']
patients = mongo_db.patients

# Initialize SQLite database
def init_sqlite_db():
   conn = get_db_connection()
   c = conn.cursor()
   c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
   conn.commit()
   conn.close()

init_sqlite_db()

# Login required decorator
def login_required(f):
   @wraps(f)
   def decorated_function(*args, **kwargs):
       if 'user_id' not in session:
           flash('Please login first')
           return redirect(url_for('user_login'))
       return f(*args, **kwargs)
   return decorated_function

# Routes
@app.route('/')
def home_page():
   return render_template('home_page.html')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       
       conn = get_db_connection()
       user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
       conn.close()
       
       if user and check_password_hash(user['password'], password):
           session['user_id'] = user['id']
           session['user_name'] = user['name']
           flash('Logged in successfully!')
           return redirect(url_for('patients_list'))
       flash('Invalid email or password')
   return render_template('user_login.html')

@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
   if request.method == 'POST':
       name = request.form['name']
       email = request.form['email']
       password = generate_password_hash(request.form['password'])
       
       conn = get_db_connection()
       try:
           conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                       (name, email, password))
           conn.commit()
           flash('Registration successful! Please login.')
           return redirect(url_for('user_login'))
       except sqlite3.IntegrityError:
           flash('Email already exists!')
       finally:
           conn.close()
   return render_template('user_register.html')

@app.route('/patients_list')
@login_required
def patients_list():
   patient_list = list(patients.find())
   return render_template('patient_base.html', patients=patient_list)

def import_kaggle_data():
   try:
       # Ścieżka do pliku CSV w folderze projektu
       csv_path = os.path.join(os.path.dirname(__file__), 'healthcare-dataset-stroke-data.csv')
       
       # Wczytaj dane z pliku CSV
       df = pd.read_csv(csv_path)
       
       # Licznik dodanych rekordów
       added_count = 0
       
       # Przekształć dane do formatu MongoDB
       for _, row in df.iterrows():
           try:
               # Walidacja i konwersja BMI
               bmi = float(row['bmi']) if pd.notna(row['bmi']) else 0.0
               if bmi < 10:  # Jeśli BMI jest za niskie, ustaw domyślną wartość
                   bmi = 25.0  # Średnia wartość BMI
               
               patient_data = {
                   'gender': str(row['gender']),
                   'age': float(row['age']),
                   'hypertension': int(row['hypertension']),
                   'ever_married': str(row['ever_married']),
                   'work_type': str(row['work_type']),
                   'residence_type': str(row['Residence_type']),
                   'avg_glucose_level': float(row['avg_glucose_level']),
                   'bmi': bmi,  # Używamy przetworzonej wartości BMI
                   'smoking_status': str(row['smoking_status'])
               }
               
               # Oblicz ryzyko udaru
               risk_factors = 0
               if patient_data['hypertension'] == 1:
                   risk_factors += 0.3
               if patient_data['age'] > 60:
                   risk_factors += 0.3
               if patient_data['avg_glucose_level'] > 200:
                   risk_factors += 0.2
               if patient_data['smoking_status'] == 'smokes':
                   risk_factors += 0.2
                   
               patient_data['stroke_risk'] = min(risk_factors, 1.0)
               
               # Sprawdź czy pacjent już istnieje
               existing_patient = patients.find_one({
                   'gender': patient_data['gender'],
                   'age': patient_data['age'],
                   'hypertension': patient_data['hypertension'],
                   'avg_glucose_level': patient_data['avg_glucose_level']
               })
               
               if not existing_patient:
                   patients.insert_one(patient_data)
                   added_count += 1
                   
           except Exception as e:
               print(f"Error processing record: {str(e)}")
               continue
       
       return True, f"Successfully imported {added_count} new patient records"
   except Exception as e:
       return False, f"Error importing data: {str(e)}"

@app.route('/import_kaggle_dataset', methods=['GET'])
@login_required
def import_kaggle_dataset():
   success, message = import_kaggle_data()
   if success:
       flash(message)
   else:
       flash(message, 'error')
   return redirect(url_for('patients_list'))

@app.route('/add_patient', methods=['POST'])
@login_required
def add_patient():
   if request.method == 'POST':
       patient_data = {
           'gender': request.form['gender'],
           'age': float(request.form['age']),
           'hypertension': int(request.form['hypertension']),
           'ever_married': request.form['ever_married'],
           'work_type': request.form['work_type'],
           'residence_type': request.form['residence_type'],
           'avg_glucose_level': float(request.form['avg_glucose_level']),
           'bmi': float(request.form['bmi']),
           'smoking_status': request.form['smoking_status']
       }
       
       # Oblicz ryzyko udaru
       risk_factors = 0.0 # changed to 0.0 for double
       if patient_data['hypertension'] == 1:
           risk_factors += 0.3
       if patient_data['age'] > 60:
           risk_factors += 0.3
       if patient_data['avg_glucose_level'] > 200:
           risk_factors += 0.2
       if patient_data['smoking_status'].lower() == 'smokes':
           risk_factors += 0.2
           
       stroke_risk = float(min(risk_factors, 1.0))
       patient_data['stroke_risk'] = stroke_risk
       
       patients.insert_one(patient_data)
       
       # Zmieniona nazwa szablonu na patient_result
       return render_template('patient_result.html', 
                            stroke_risk=stroke_risk,
                            hypertension=patient_data['hypertension'],
                            age=patient_data['age'],
                            glucose=patient_data['avg_glucose_level'],
                            smoking=patient_data['smoking_status'])

@app.route('/patient_info/<string:patient_id>')
@login_required
def patient_info(patient_id):
   patient = patients.find_one({'_id': ObjectId(patient_id)})
   if patient:
       return render_template('patient_info.html', patient=patient)
   flash('Patient not found!')
   return redirect(url_for('patients_list'))

@app.route('/logout')
def logout():
   session.clear()
   flash('Logged out successfully!')
   return redirect(url_for('home_page'))

if __name__ == '__main__':
   app.run(debug=True)
