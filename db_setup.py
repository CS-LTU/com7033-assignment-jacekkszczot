import sqlite3
from pymongo import MongoClient
import os

def setup_sqlite():
    conn = sqlite3.connect('user_base.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def setup_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['stroke_management']
    db.create_collection('patients')
    db.command({
        'collMod': 'patients',
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['gender', 'age', 'hypertension', 'avg_glucose_level', 'bmi'],
                'properties': {
                    'gender': {
                        'bsonType': 'string',
                        'enum': ['Male', 'Female', 'Other']
                    },
                    'age': {
                        'bsonType': 'double',
                        'minimum': 0,
                        'maximum': 120
                    },
                    'hypertension': {
                        'bsonType': 'int',
                        'enum': [0, 1]
                    },
                    'ever_married': {
                        'bsonType': 'string',
                        'enum': ['Yes', 'No']
                    },
                    'work_type': {
                        'bsonType': 'string'
                    },
                    'residence_type': {
                        'bsonType': 'string',
                        'enum': ['Rural', 'Urban']
                    },
                    'avg_glucose_level': {
                        'bsonType': ['double', 'init'] #  to accept both int and double ['double', 'init']
                        'minimum': 0
                    },
                    'bmi': {
                        'bsonType': ['double', 'init'] # to accept both int and double ['double', 'init']
                        'minimum': 10,
                        'maximum': 50
                    },
                    'smoking_status': {
                        'bsonType': 'string',
                        'enum': ['formerly smoked', 'never smoked', 'smokes', 'Unknown']
                    },
                    'stroke_risk': {
                        'bsonType': ['double', 'init'] # to accept both int and double ['double', 'init']
                        'minimum': 0,
                        'maximum': 1
                    }
                }
            }
        }
    })

def init_databases():
    try:
        setup_sqlite()
        print("SQLite database setup complete")
        
        setup_mongodb()
        print("MongoDB setup complete")
        
    except Exception as e:
        print(f"Error setting up databases: {e}")

# Database connection functions
def get_db_connection():
    conn = sqlite3.connect('user_base.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_mongodb_connection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['stroke_management']
    return db

if __name__ == "__main__":
    init_databases()