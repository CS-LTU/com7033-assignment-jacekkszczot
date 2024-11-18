# db_operations.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from db_setup import get_db_connection, get_mongodb_connection

# User Operations (SQLite)
def add_user(name, email, password):
    """Add new user to SQLite database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        hashed_password = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, hashed_password)
        )
        conn.commit()
        return True, "User registered successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def verify_user(email, password):
    """Verify user login"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        user = cursor.execute(
            'SELECT * FROM users WHERE email = ?', 
            (email,)
        ).fetchone()
        
        if user and check_password_hash(user['password'], password):
            return True, user['id']
        return False, None
    finally:
        conn.close()

# Patient Operations (MongoDB)
def add_patient(patient_data):
    """Add new patient to MongoDB"""
    db = get_mongodb_connection()
    try:
        result = db.patients.insert_one(patient_data)
        return True, str(result.inserted_id)
    except Exception as e:
        return False, str(e)

def get_patient(patient_id):
    """Get patient by ID"""
    db = get_mongodb_connection()
    try:
        patient = db.patients.find_one({'_id': patient_id})
        return patient
    except Exception as e:
        return None

def get_all_patients():
    """Get all patients"""
    db = get_mongodb_connection()
    try:
        patients = list(db.patients.find())
        return patients
    except Exception as e:
        return []

def update_patient(patient_id, updated_data):
    """Update patient data"""
    db = get_mongodb_connection()
    try:
        result = db.patients.update_one(
            {'_id': patient_id},
            {'$set': updated_data}
        )
        return bool(result.modified_count)
    except Exception as e:
        return False

def delete_patient(patient_id):
    """Delete patient"""
    db = get_mongodb_connection()
    try:
        result = db.patients.delete_one({'_id': patient_id})
        return bool(result.deleted_count)
    except Exception as e:
        return False
