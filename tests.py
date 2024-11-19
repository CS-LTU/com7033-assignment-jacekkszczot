import unittest
from main_app import app

class StrokeAppTests(unittest.TestCase):
    def setUp(self):
       app.config['TESTING'] = True
       self.app = app.test_client()
       self.username = "Jacek"    
       self.email = "jacek@jacek.com" 
        
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
    def test_user_exists(self):
       self.app.post('/user_register', data={
           'name': self.username,
           'email': self.email,
           'password': 'test123'
       })
       self.assertTrue(user_exists(self.username, self.email))

   def test_user_not_exists(self):
       self.assertFalse(user_exists('NonExistenUser', 'nonexistent@example.com'))

if __name__ == '__main__':
    unittest.main()
