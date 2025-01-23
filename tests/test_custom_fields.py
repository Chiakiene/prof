import unittest
from main import app, db, User, CustomField
from werkzeug.security import generate_password_hash

class CustomFieldsTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            self.create_test_user()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_user(self):
        with app.app_context():
            user = User(
                username='testuser',
                password=generate_password_hash('testpass'),
                email='test@example.com',
                user_id='test1234'
            )
            db.session.add(user)
            db.session.commit()

    def test_add_custom_field(self):
        # ログイン
        self.app.post('/', data={
            'username': 'testuser',
            'password': 'testpass'
        })

        # カスタムフィールドの追加
        response = self.app.post('/profile', data={
            'user_id': 'test1234',
            'username': 'testuser',
            'email': 'test@example.com',
            'custom_labels[]': ['Test Label'],
            'custom_values[]': ['Test Value'],
            'custom_ids[]': ['']
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with app.app_context():
            field = CustomField.query.filter_by(label='Test Label').first()
            self.assertIsNotNone(field)
            self.assertEqual(field.value, 'Test Value')

    def test_max_custom_fields(self):
        # ログイン
        self.app.post('/', data={
            'username': 'testuser',
            'password': 'testpass'
        })

        # 21個のフィールドを追加
        labels = ['field' + str(i) for i in range(21)]
        values = ['value' + str(i) for i in range(21)]
        ids = [''] * 21

        response = self.app.post('/profile', data={
            'user_id': 'test1234',
            'username': 'testuser',
            'email': 'test@example.com',
            'custom_labels[]': labels,
            'custom_values[]': values,
            'custom_ids[]': ids
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200) 