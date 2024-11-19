import unittest
from main_app import app

class StrokeAppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
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
        response = self.app.get('/user_register')
        self.assertEqual(response.status_code, 200)  
        
    def test_login(self):
        response = self.app.get('/user_login')
        self.assertEqual(response.status_code, 200)  

if __name__ == '__main__':
    unittest.main()