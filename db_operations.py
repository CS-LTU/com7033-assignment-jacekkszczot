# db_operations.py
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

def get_all_patients():
    """Get all patients"""
    db = get_mongodb_connection()
    try:
        patients = list(db.patients.find())
        return patients
    except Exception as e:
        return []