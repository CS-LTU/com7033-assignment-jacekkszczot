# db_setup.py
import sqlite3
from pymongo import MongoClient

def setup_sqlite():
    """Setup SQLite database for users"""
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
    """Setup MongoDB for patient data"""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['stroke_management']
    
    # Create patient collection
    db.create_collection('patients')

def init_databases():
    """Initialize both databases"""
    try:
        setup_sqlite()
        print("SQLite database setup complete")
        setup_mongodb()
        print("MongoDB setup complete")
    except Exception as e:
        print(f"Error setting up databases: {e}")

def get_db_connection():
    """Get SQLite connection for users"""
    conn = sqlite3.connect('user_base.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_mongodb_connection():
    """Get MongoDB connection for patients"""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['stroke_management']
    return db

if __name__ == "__main__":
    init_databases()