from main import create_app
from extensions import db
from models import User, UserDesign, CustomField
import os

def recreate_database():
    # アプリケーションコンテキストを取得
    app = create_app()
    
    with app.app_context():
        # データベースファイルが存在する場合は削除
        if os.path.exists('users.db'):
            os.remove('users.db')
            print('既存のデータベースを削除しました')
        
        # データベースとテーブルを作成
        db.create_all()
        print('データベースとテーブルを作成しました')
        
        # テスト用のユーザーを作成
        test_user = User(
            username='test_user',
            email='test@example.com',
            user_id='test123'
        )
        test_user.set_password('pass')
        
        # デザイン設定を追加
        test_design = UserDesign(
            user=test_user,
            background_type='color',
            background_color='#f0f0f0',
            font_family="'Noto Sans JP', sans-serif",
            font_size=16,
            text_color='#333333'
        )
        
        # カスタムフィールドを追加
        custom_fields = [
            CustomField(
                user=test_user,
                label='趣味',
                value='プログラミング',
                order=0
            ),
            CustomField(
                user=test_user,
                label='好きな言語',
                value='Python',
                order=1
            )
        ]
        
        # データベースに保存
        db.session.add(test_user)
        db.session.add(test_design)
        for field in custom_fields:
            db.session.add(field)
        
        try:
            db.session.commit()
            print('テストユーザーを作成しました:')
            print(f'ユーザー名: {test_user.username}')
            print(f'パスワード: pass')
            print(f'メール: {test_user.email}')
        except Exception as e:
            db.session.rollback()
            print(f'エラーが発生しました: {str(e)}')

if __name__ == '__main__':
    recreate_database()