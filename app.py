import os
from flask import Flask
from extensions import init_app, markdown_filter
from routes import auth_bp, profile_bp
from models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Jinja2フィルターを直接登録
    app.jinja_env.filters['markdown'] = markdown_filter
    
    # アップロード関連の設定
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 最大5MB
    
    # アップロードフォルダが存在しない場合は作成
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    # 拡張機能の初期化
    init_app(app)
    
    # Blueprint登録
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp, url_prefix='/profile')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 