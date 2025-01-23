import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from main import app, db
import os

@pytest.fixture(scope='session')
def driver():
    """Seleniumのドライバーを提供"""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # ヘッドレスモードで実行
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope='session')
def test_client():
    """Flaskのテストクライアントを提供"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def auth(test_client):
    """認証用のヘルパー関数"""
    class AuthActions:
        def register(self, username='testuser', password='password', email='test@example.com'):
            return test_client.post('/register', data={
                'username': username,
                'password': password,
                'email': email
            }, follow_redirects=True)
            
        def login(self, username='testuser', password='password'):
            return test_client.post('/', data={
                'username': username,
                'password': password
            }, follow_redirects=True)
            
        def logout(self):
            return test_client.get('/logout', follow_redirects=True)
    
    return AuthActions() 