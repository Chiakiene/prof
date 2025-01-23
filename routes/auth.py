from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User
import random
import string
from datetime import datetime, timedelta
from flask_mail import Message
from extensions import mail

auth_bp = Blueprint('auth', __name__)

def generate_user_id(username):
    """ユーザーIDを生成"""
    # ユーザー名をベースにしたユーザーID
    base_id = username.lower()
    # ランダムな4桁の数字を追加
    random_digits = ''.join(random.choices(string.digits, k=4))
    user_id = f"{base_id}{random_digits}"
    
    # 既に存在する場合は再生成
    while User.query.filter_by(user_id=user_id).first():
        random_digits = ''.join(random.choices(string.digits, k=4))
        user_id = f"{base_id}{random_digits}"
    
    return user_id

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # パスワードの長さチェック
        if len(password) < 4:
            flash('パスワードは4文字以上で入力してください', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('このユーザー名は既に使用されています', 'error')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first():
            flash('このメールアドレスは既に登録されています', 'error')
            return redirect(url_for('auth.register'))
        
        # ユーザーIDを生成
        user_id = generate_user_id(username)
        
        # ユーザーを作成
        user = User(
            user_id=user_id,
            username=username,
            email=email
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('アカウントを作成しました', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile.index'))
        
    if request.method == 'POST':
        login_id = request.form.get('login_id')  # メールアドレスまたはユーザーID
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        # メールアドレスまたはユーザーIDでユーザーを検索
        user = User.query.filter(
            db.or_(
                User.email == login_id,
                User.user_id == login_id
            )
        ).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            return redirect(url_for('profile.index'))
            
        flash('ログインIDまたはパスワードが正しくありません', 'error')
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('profile.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = user.generate_reset_token()
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            
            # メール送信
            msg = Message('パスワードリセット',
                         sender='noreply@example.com',
                         recipients=[user.email])
            msg.body = f'''パスワードをリセットするには、以下のリンクをクリックしてください：

{reset_url}

このリンクは24時間有効です。
'''
            mail.send(msg)
            
            flash('パスワードリセットの手順をメールで送信しました', 'success')
            return redirect(url_for('auth.login'))
            
        flash('このメールアドレスは登録されていません', 'error')
        
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('profile.index'))
        
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.verify_reset_token(token):
        flash('無効または期限切れのリンクです', 'error')
        return redirect(url_for('auth.forgot_password'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        
        if len(password) < 4:
            flash('パスワードは4文字以上で入力してください', 'error')
            return redirect(url_for('auth.reset_password', token=token))
            
        user.set_password(password)
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()
        
        flash('パスワードを更新しました', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/reset_password.html') 