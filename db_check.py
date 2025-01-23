from flask import Flask
from models import db, User
from datetime import datetime
import os

def check_db():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    
    with app.app_context():
        try:
            # ユーザー一覧を取得
            users = User.query.all()
            
            print('\nデータベース内のユーザー:')
            for user in users:
                print(f'\nユーザーID: {user.id}')
                print(f'ユーザー名: {user.username}')
                print(f'メール: {user.email}')
                print(f'プロフィール:')
                print(f'  自己紹介: {user.bio or "未設定"}')
                print(f'  場所: {user.location or "未設定"}')
                print(f'  Webサイト: {user.website or "未設定"}')
                print(f'  アバター: {user.avatar_url or "未設定"}')
                print(f'作成日時: {user.created_at}')
                print(f'更新日時: {user.updated_at}')
                
        except Exception as e:
            print(f'エラーが発生しました: {str(e)}')

def check_upload_directories():
    """アップロードディレクトリの状態を確認"""
    print("\n=== アップロードディレクトリの確認 ===")
    
    # アバター画像ディレクトリ
    avatar_dir = os.path.join('static', 'uploads')
    print(f"\nアバター画像ディレクトリ ({avatar_dir}):")
    if os.path.exists(avatar_dir):
        files = os.listdir(avatar_dir)
        print(f"ファイル数: {len(files)}")
        for file in files:
            print(f"- {file}")
    else:
        print("ディレクトリが存在しません")

    # 背景画像ディレクトリ
    bg_dir = os.path.join('static', 'uploads', 'backgrounds')
    print(f"\n背景画像ディレクトリ ({bg_dir}):")
    if os.path.exists(bg_dir):
        files = os.listdir(bg_dir)
        print(f"ファイル数: {len(files)}")
        for file in files:
            print(f"- {file}")
    else:
        print("ディレクトリが存在しません")

if __name__ == '__main__':
    check_db()
    check_upload_directories() 