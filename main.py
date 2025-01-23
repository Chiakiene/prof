from flask import Flask, redirect, url_for
from extensions import db, login_manager, migrate, mail
from config import Config
from models import User  # Userモデルをインポート
from routes.auth import auth_bp
from routes.profile import profile_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 拡張機能の初期化
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Blueprintの登録
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')

    # ルートページのリダイレクト
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # ログインマネージャーの設定
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'このページにアクセスするにはログインが必要です。'
    login_manager.login_message_category = 'warning'

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
