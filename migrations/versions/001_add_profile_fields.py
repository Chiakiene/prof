"""Add profile fields

Revision ID: 001
Revises: 
Create Date: 2024-03-14
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 既存のテーブルをバックアップ
    op.rename_table('users', 'users_backup')
    
    # 新しいテーブルを作成
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(20), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('password_hash', sa.String(128)),
        sa.Column('bio', sa.Text()),
        sa.Column('location', sa.String(100)),
        sa.Column('website', sa.String(200)),
        sa.Column('avatar_url', sa.String(200)),
        sa.Column('created_at', sa.DateTime(), nullable=False, 
                  server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, 
                  server_default=sa.func.current_timestamp()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    
    # データを移行
    op.execute(
        'INSERT INTO users (id, username, email, password_hash, created_at) '
        'SELECT id, username, email, password_hash, created_at FROM users_backup'
    )
    
    # バックアップテーブルを削除
    op.drop_table('users_backup')

def downgrade():
    # 元のテーブル構造に戻す
    op.rename_table('users', 'users_backup')
    
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(20), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('password_hash', sa.String(128)),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    
    # データを戻す
    op.execute(
        'INSERT INTO users (id, username, email, password_hash, created_at) '
        'SELECT id, username, email, password_hash, created_at FROM users_backup'
    )
    
    # バックアップテーブルを削除
    op.drop_table('users_backup') 