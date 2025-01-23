from flask import Flask
from models import db, User, CustomField
from datetime import datetime
import os
from sqlalchemy import inspect

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

def check_table_columns():
    """データベースのテーブルとカラムを確認"""
    inspector = inspect(db.engine)
    
    print("\n=== データベース構造 ===\n")
    
    for table_name in inspector.get_table_names():
        print(f"\n📋 テーブル: {table_name}")
        print("─" * 50)
        
        # カラム情報を取得
        columns = inspector.get_columns(table_name)
        for column in columns:
            nullable = "NULL可" if column['nullable'] else "NULL不可"
            default = f"デフォルト: {column['default']}" if column['default'] is not None else ""
            
            print(f"  ├─ {column['name']}")
            print(f"  │  型: {column['type']}")
            print(f"  │  {nullable} {default}")
        
        # 外部キー制約を取得
        foreign_keys = inspector.get_foreign_keys(table_name)
        if foreign_keys:
            print("\n  🔗 外部キー:")
            for fk in foreign_keys:
                print(f"  ├─ {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        # インデックスを取得
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print("\n  📑 インデックス:")
            for idx in indexes:
                unique = "ユニーク" if idx['unique'] else "非ユニーク"
                print(f"  ├─ {idx['name']} ({unique})")
                print(f"  │  カラム: {', '.join(idx['column_names'])}")

def check_model_columns():
    """Modelで定義されているカラムを確認"""
    models = [User, CustomField]
    
    print("\n=== Model定義 ===\n")
    
    for model in models:
        print(f"\n📝 Model: {model.__name__}")
        print("─" * 50)
        
        for column in model.__table__.columns:
            nullable = "NULL可" if column.nullable else "NULL不可"
            default = f"デフォルト: {column.default}" if column.default is not None else ""
            
            print(f"  ├─ {column.name}")
            print(f"  │  型: {column.type}")
            print(f"  │  {nullable} {default}")
        
        # リレーションシップを取得
        if hasattr(model, '__mapper__'):
            relationships = model.__mapper__.relationships
            if relationships:
                print("\n  🔗 リレーションシップ:")
                for name, rel in relationships.items():
                    print(f"  ├─ {name} -> {rel.target}")

if __name__ == '__main__':
    check_db()
    check_upload_directories()
    with app.app_context():
        print("\n🔍 データベース構造を確認中...\n")
        check_table_columns()
        check_model_columns() 