from flask import Flask
from models import db, User  # UserDesignとCustomFieldを削除
from datetime import datetime

def init_db():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    
    with app.app_context():
        # データベースを作成
        db.drop_all()  # 既存のテーブルを削除
        db.create_all()
        
        # 管理者ユーザーを作成
        admin_user = User(
            user_id='admin',  # ユーザーID追加
            username='admin',
            email='admin@example.com',
            bio='管理者アカウントです',
            location='東京',
            website='https://admin.example.com',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        admin_user.set_password('admin')  # 4文字
        
        # 一般ユーザーを作成
        users = [
            {
                'user_id': 'yamada123',  # ユーザーID追加
                'username': 'yamada',
                'email': 'yamada@example.com',
                'password': 'yamada1234',
                'bio': '山田です。よろしくお願いします。',
                'location': '大阪',
                'website': 'https://yamada.example.com'
            },
            {
                'user_id': 'tanaka456',  # ユーザーID追加
                'username': 'tanaka',
                'email': 'tanaka@example.com',
                'password': 'tanaka1234',
                'bio': '田中と申します。プログラミング勉強中です。',
                'location': '福岡',
                'website': 'https://tanaka.example.com'
            },
            {
                'user_id': 'suzuki789',  # ユーザーID追加
                'username': 'suzuki',
                'email': 'suzuki@example.com',
                'password': 'suzuki1234',
                'bio': '鈴木です。写真が趣味です。',
                'location': '名古屋',
                'website': 'https://suzuki.example.com'
            }
        ]
        
        # データベースに保存
        db.session.add(admin_user)
        for user in users:
            new_user = User(
                user_id=user['user_id'],
                username=user['username'],
                email=user['email'],
                bio=user['bio'],
                location=user['location'],
                website=user['website'],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            new_user.set_password(user['password'])
            db.session.add(new_user)
        
        try:
            db.session.commit()
            print('データベースを初期化しました')
            print('\n管理者アカウント:')
            print(f'ユーザー名: {admin_user.username}')
            print(f'パスワード: admin')
            print(f'メール: {admin_user.email}')
            print('\n一般ユーザー:')
            for user in users:
                print(f'ユーザー名: {user["username"]}')
                print(f'パスワード: {user["password"]}')
                print(f'メール: {user["email"]}')
        except Exception as e:
            db.session.rollback()
            print(f'エラーが発生しました: {str(e)}')

if __name__ == '__main__':
    init_db() 