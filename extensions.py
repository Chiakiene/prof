from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

# データベース
db = SQLAlchemy()

# ログイン管理
login_manager = LoginManager()
login_manager.login_view = 'login'

# マイグレーション
migrate = Migrate()

# Flask-Mailを追加
mail = Mail() 