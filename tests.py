# tests.py
import unittest
from main_app import app
from werkzeug.security import generate_password_hash
import json

class StrokeAppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_login_page(self):
        response = self.app.get('/user_login')
        self.assertEqual(response.status_code, 200)
        
    def test_register_page(self):
        response = self.app.get('/user_register')
        self.assertEqual(response.status_code, 200)
        
    def test_patient_list_redirect_when_not_logged_in(self):
        response = self.app.get('/patients_list')
        self.assertEqual(response.status_code, 302)
        
    def test_registration(self):
        response = self.app.post('/user_register', data={
            'name': 'Test User',
            'email': 'test@test.com',
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 302)
        
    def test_login(self):
        response = self.app.post('/user_login', data={
            'email': 'test@test.com',
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()