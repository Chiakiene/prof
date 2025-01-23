"""Add reset token columns

Revision ID: 002
Revises: 001
Create Date: 2024-03-14
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # パスワードリセット用のカラムを追加
    op.add_column('users', sa.Column('reset_token', sa.String(100), unique=True, nullable=True))
    op.add_column('users', sa.Column('reset_token_expires', sa.DateTime, nullable=True))

def downgrade():
    # パスワードリセット用のカラムを削除
    op.drop_column('users', 'reset_token')
    op.drop_column('users', 'reset_token_expires') 