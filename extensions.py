from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
import markdown2

# データベース
db = SQLAlchemy()

# ログイン管理
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'ログインが必要です'

# マイグレーション
migrate = Migrate()

# Flask-Mailを追加
mail = Mail()

def markdown_filter(text):
    """安全なMarkdown変換を行うフィルター"""
    if text is None:
        return ''
    return markdown2.markdown(text, 
        safe_mode=True,  # 安全なHTML出力
        extras=[
            "fenced-code-blocks",  # コードブロック
            "tables",             # テーブル
            "break-on-newline",   # 改行
            "header-ids",         # ヘッダーID
            "strike",            # 取り消し線
            "target-blank-links"  # 外部リンクを新しいタブで開く
        ]
    )

def init_app(app: Flask):
    """拡張機能の初期化"""
    # データベース初期化
    db.init_app(app)
    migrate.init_app(app, db)
    
    # ログイン管理の設定
    login_manager.init_app(app)
    
    # メール機能の初期化
    mail.init_app(app)
    
    return app 