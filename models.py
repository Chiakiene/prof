from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from extensions import db
import random
import string

class CustomField(db.Model):
    __tablename__ = 'custom_fields'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    label = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(500), nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # リレーションシップ
    user = db.relationship('User', backref=db.backref('custom_fields', lazy=True))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # プロフィール情報
    bio = db.Column(db.Text(1000))
    location = db.Column(db.String(100))
    website = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255))
    
    # タイムスタンプ
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # パスワードリセット用
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expires = db.Column(db.DateTime)

    def set_password(self, password):
        """パスワードをハッシュ化して設定"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """パスワードをチェック"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """ユーザー情報を辞書形式で返す"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'bio': self.bio,
            'location': self.location,
            'website': self.website,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<User {self.username}>'

    def generate_reset_token(self):
        """パスワードリセット用のトークンを生成"""
        self.reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=24)  # 24時間有効
        db.session.commit()
        return self.reset_token
    
    def verify_reset_token(self, token):
        """リセットトークンを検証"""
        if (self.reset_token != token or 
            self.reset_token_expires < datetime.utcnow()):
            return False
        return True

    def update_user_id(self, new_user_id):
        """ユーザーIDを更新"""
        if User.query.filter(User.user_id == new_user_id, User.id != self.id).first():
            return False, 'このユーザーIDは既に使用されています'
        self.user_id = new_user_id
        db.session.commit()
        return True, 'ユーザーIDを更新しました' 