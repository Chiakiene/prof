from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
from main import app, db, User, UserDesign, CustomField, SponsorshipTier
from flask_login import current_user
from werkzeug.security import generate_password_hash

def test_profile_update(test_client, auth, driver):
    """Test profile update"""
    auth.register()
    auth.login()
    
    response = test_client.post('/profile', data={
        'user_id': 'testuser123',
        'username': 'testuser',
        'email': 'test@example.com',
        'bio': 'Test bio',
        'location': 'Tokyo',
        'website': 'https://example.com'
    }, follow_redirects=True)
    
    assert b'Profile updated successfully' in response.data

def test_profile_design(driver):
    """プロフィールデザインのテスト"""
    driver.get('http://localhost:5000/profile')
    
    # 背景色の変更
    color_input = driver.find_element(By.ID, 'background_color')
    color_input.send_keys('#ff0000')
    
    # プレビューの確認
    preview = driver.find_element(By.ID, 'designPreview')
    assert 'rgb(255, 0, 0)' in preview.value_of_css_property('background-color')

class ProfileTestCase(unittest.TestCase):
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

    def test_profile_update_basic(self):
        """Test basic profile information update"""
        # Login
        self.app.post('/', data={
            'username': 'testuser',
            'password': 'testpass'
        })

        # Update profile
        response = self.app.post('/profile', data={
            'user_id': 'test1234',
            'username': 'testuser',
            'email': 'test@example.com',
            'bio': 'Test bio',
            'location': 'Test location',
            'website': 'http://test.com'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertEqual(user.bio, 'Test bio')
            self.assertEqual(user.location, 'Test location')

    def test_profile_design_update(self):
        """Test profile design settings update"""
        # Login
        self.app.post('/', data={
            'username': 'testuser',
            'password': 'testpass'
        })

        # Update design settings
        response = self.app.post('/profile', data={
            'user_id': 'test1234',
            'username': 'testuser',
            'email': 'test@example.com',
            'background_type': 'color',
            'background_color': '#ff0000',
            'text_color': '#000000',
            'accent_color': '#0000ff',
            'background_opacity': '80'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with app.app_context():
            design = UserDesign.query.filter_by(user_id=1).first()
            self.assertIsNotNone(design)
            self.assertEqual(design.background_color, '#ff0000')
            self.assertEqual(design.text_color, '#000000')

    def test_invalid_profile_update(self):
        """Test invalid profile update attempts"""
        # Login
        self.app.post('/', data={
            'username': 'testuser',
            'password': 'testpass'
        })

        # Test with invalid user_id
        response = self.app.post('/profile', data={
            'user_id': 'test!@#$',  # Invalid characters
            'username': 'testuser',
            'email': 'test@example.com'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)

    def test_data_persistence(self):
        """Test if all data is properly saved to database"""
        # Login
        self.app.post('/', data={
            'username': 'testuser',
            'password': 'testpass'
        })

        # Update all possible fields
        test_data = {
            'user_id': 'test1234',
            'username': 'testuser',
            'email': 'test@example.com',
            'bio': 'Test bio',
            'location': 'Test location',
            'website': 'http://test.com',
            # Design settings
            'background_type': 'color',
            'background_color': '#ff0000',
            'text_color': '#000000',
            'accent_color': '#0000ff',
            'background_opacity': '80',
            # Custom fields
            'custom_labels[]': ['Field1', 'Field2'],
            'custom_values[]': ['Value1', 'Value2'],
            'custom_ids[]': ['', ''],
            # Sponsorship settings
            'tier_names[]': ['Basic', 'Premium'],
            'tier_min_prices[]': ['500', '1000'],
            'tier_suggested_prices[]': ['1000', '2000'],
            'tier_descriptions[]': ['Basic tier', 'Premium tier'],
            'tier_active[]': ['on', 'on']
        }

        response = self.app.post('/profile', data=test_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verify all data is saved correctly
        with app.app_context():
            # User data
            user = User.query.filter_by(username='testuser').first()
            self.assertEqual(user.bio, 'Test bio')
            self.assertEqual(user.location, 'Test location')
            self.assertEqual(user.website, 'http://test.com')

            # Design data
            design = UserDesign.query.filter_by(user_id=user.id).first()
            self.assertIsNotNone(design)
            self.assertEqual(design.background_color, '#ff0000')
            self.assertEqual(design.text_color, '#000000')
            self.assertEqual(design.accent_color, '#0000ff')
            self.assertEqual(design.background_opacity, 0.8)

            # Custom fields
            custom_fields = CustomField.query.filter_by(user_id=user.id).all()
            self.assertEqual(len(custom_fields), 2)
            self.assertEqual(custom_fields[0].label, 'Field1')
            self.assertEqual(custom_fields[0].value, 'Value1')

            # Sponsorship tiers
            tiers = SponsorshipTier.query.filter_by(user_id=user.id).all()
            self.assertEqual(len(tiers), 2)
            self.assertEqual(tiers[0].name, 'Basic')
            self.assertEqual(tiers[0].min_price, 500)
            self.assertEqual(tiers[0].suggested_price, 1000)

    def test_basic_info_update(self):
        """Test basic information update"""
        # Login
        self.app.post('/', data={
            'username': 'testuser',
            'password': 'testpass'
        })

        # Update basic info
        test_data = {
            'user_id': 'test1234',
            'username': 'testuser_updated',
            'email': 'updated@example.com',
            'bio': 'Updated bio',
            'location': 'Updated location',
            'website': 'http://updated.com'
        }

        response = self.app.post('/profile', data=test_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verify updates
        with app.app_context():
            user = User.query.filter_by(id=1).first()
            self.assertEqual(user.username, 'testuser_updated')
            self.assertEqual(user.email, 'updated@example.com')
            self.assertEqual(user.bio, 'Updated bio')
            self.assertEqual(user.location, 'Updated location')
            self.assertEqual(user.website, 'http://updated.com') 