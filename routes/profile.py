from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
from datetime import datetime
from models import db, User, CustomField

profile_bp = Blueprint('profile', __name__)

def allowed_file(filename):
    """アップロードされたファイルが許可された拡張子か確認"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@profile_bp.route('/')
@login_required
def index():
    """プロフィールページを表示"""
    return render_template('profile.html', user=current_user)

@profile_bp.route('/update', methods=['POST'])
@login_required
def update():
    """プロフィール情報を更新"""
    try:
        username = request.form.get('username')
        user_id = request.form.get('user_id')
        email = request.form.get('email')
        bio = request.form.get('bio', '')
        location = request.form.get('location', '')
        website = request.form.get('website', '').strip()

        # 文字数制限のバリデーション
        if not username or len(username) < 3 or len(username) > 50:
            flash('ユーザー名は3文字以上50文字以内で入力してください', 'error')
            return redirect(url_for('profile.index'))

        if not user_id or len(user_id) < 3 or len(user_id) > 30:
            flash('ユーザーIDは3文字以上30文字以内で入力してください', 'error')
            return redirect(url_for('profile.index'))

        if len(email) > 255:
            flash('メールアドレスが長すぎます', 'error')
            return redirect(url_for('profile.index'))

        if len(bio) > 1000:
            flash('自己紹介は1000文字以内で入力してください', 'error')
            return redirect(url_for('profile.index'))

        if len(location) > 100:
            flash('場所は100文字以内で入力してください', 'error')
            return redirect(url_for('profile.index'))

        if len(website) > 255:
            flash('WebサイトのURLが長すぎます', 'error')
            return redirect(url_for('profile.index'))

        # 重複チェック
        if username != current_user.username and User.query.filter_by(username=username).first():
            flash('このユーザー名は既に使用されています', 'error')
            return redirect(url_for('profile.index'))

        if user_id != current_user.user_id and User.query.filter_by(user_id=user_id).first():
            flash('このユーザーIDは既に使用されています', 'error')
            return redirect(url_for('profile.index'))

        if email != current_user.email and User.query.filter_by(email=email).first():
            flash('このメールアドレスは既に登録されています', 'error')
            return redirect(url_for('profile.index'))

        # 基本情報の更新
        current_user.username = username
        current_user.user_id = user_id
        current_user.email = email
        current_user.bio = bio
        current_user.location = location

        # WebサイトのURL検証
        if website and not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        current_user.website = website

        # カスタムフィールドの更新
        CustomField.query.filter_by(user_id=current_user.id).delete()
        fields = []
        for i in range(20):
            label = request.form.get(f'label_{i}')
            value = request.form.get(f'value_{i}')
            if label and value:
                field = CustomField(
                    user_id=current_user.id,
                    label=label,
                    value=value,
                    order=i
                )
                fields.append(field)

        if len(fields) > 20:
            flash('カスタムフィールドは20個までです', 'error')
            return redirect(url_for('profile.index'))

        db.session.add_all(fields)
        db.session.commit()
        flash('プロフィールを更新しました', 'success')

    except Exception as e:
        db.session.rollback()
        flash('プロフィールの更新に失敗しました', 'error')
        current_app.logger.error(f'Profile update error: {str(e)}')

    return redirect(url_for('profile.index'))

@profile_bp.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    """プロフィール画像をアップロード"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
    file = request.files['image']
    if not file or not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type'}), 400
    
    try:
        # ファイル名を安全に保存
        filename = secure_filename(f"{current_user.id}_avatar_{int(datetime.utcnow().timestamp())}.jpg")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # 古い画像を削除
        if current_user.avatar_url:
            old_file = os.path.join(current_app.root_path, 'static', current_user.avatar_url)
            if os.path.exists(old_file):
                os.remove(old_file)
        
        # 新しい画像を保存
        file.save(filepath)
        current_user.avatar_url = f'uploads/{filename}'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'url': url_for('static', filename=f'uploads/{filename}')
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Image upload error: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500

@profile_bp.route('/<username>')
def view(username):
    """ユーザーのプロフィールページを表示"""
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile/view.html', user=user)

@profile_bp.route('/update_user_id', methods=['POST'])
@login_required
def update_user_id():
    new_user_id = request.form.get('user_id')
    
    if not new_user_id:
        flash('ユーザーIDを入力してください', 'error')
        return redirect(url_for('profile.index'))
        
    if len(new_user_id) < 3 or len(new_user_id) > 20:
        flash('ユーザーIDは3文字以上20文字以内で入力してください', 'error')
        return redirect(url_for('profile.index'))
        
    success, message = current_user.update_user_id(new_user_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('profile.index'))

@profile_bp.route('/custom_fields', methods=['POST'])
@login_required
def update_custom_fields():
    # 既存のカスタムフィールドを削除
    CustomField.query.filter_by(user_id=current_user.id).delete()
    
    # 新しいカスタムフィールドを追加
    fields = []
    for i in range(20):  # 最大20個
        label = request.form.get(f'label_{i}')
        value = request.form.get(f'value_{i}')
        
        if label and value:
            field = CustomField(
                user_id=current_user.id,
                label=label,
                value=value,
                order=i
            )
            fields.append(field)
    
    if len(fields) > 20:
        flash('カスタムフィールドは20個までです', 'error')
        return redirect(url_for('profile.index'))
    
    db.session.add_all(fields)
    db.session.commit()
    
    flash('カスタムフィールドを更新しました', 'success')
    return redirect(url_for('profile.index'))

@profile_bp.errorhandler(404)
def page_not_found(e):
    """404エラーページを表示"""
    return render_template('errors/404.html'), 404