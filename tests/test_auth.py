import unittest
from main import app, db, User
from werkzeug.security import generate_password_hash

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        response = self.app.post('/register', data={
            'username': 'testuser',
            'password': 'testpass',
            'email': 'test@example.com'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)

    def test_login(self):
        with app.app_context():
            user = User(
                username='testuser',
                password=generate_password_hash('testpass'),
                email='test@example.com',
                user_id='test1234'
            )
            db.session.add(user)
            db.session.commit()

        response = self.app.post('/', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.test_login()
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_duplicate_username(self):
        self.test_register()
        response = self.app.post('/register', data={
            'username': 'testuser',
            'password': 'testpass',
            'email': 'test2@example.com'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200) 