"""initial migration

Revision ID: 7f6cfb6ec824
Revises: 
Create Date: 2025-01-24 00:08:34.126248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f6cfb6ec824'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=254), nullable=False),
    sa.Column('oauth_provider', sa.String(length=20), nullable=True),
    sa.Column('oauth_id', sa.String(length=100), nullable=True),
    sa.Column('bio', sa.String(length=1000), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('website', sa.String(length=200), nullable=True),
    sa.Column('avatar_url', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('custom_field',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=30), nullable=False),
    sa.Column('value', sa.String(length=200), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('flask_dance_oauth',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('token', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sponsorship_tier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('min_price', sa.Integer(), nullable=False),
    sa.Column('suggested_price', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_design',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('background_type', sa.String(length=20), nullable=True),
    sa.Column('background_color', sa.String(length=20), nullable=True),
    sa.Column('background_image', sa.String(length=200), nullable=True),
    sa.Column('background_opacity', sa.Float(), nullable=True),
    sa.Column('text_color', sa.String(length=20), nullable=True),
    sa.Column('accent_color', sa.String(length=20), nullable=True),
    sa.Column('font_family', sa.String(length=50), nullable=True),
    sa.Column('font_size', sa.Integer(), nullable=True),
    sa.Column('heading_size', sa.Integer(), nullable=True),
    sa.Column('text_border_enabled', sa.Boolean(), nullable=True),
    sa.Column('text_border_color', sa.String(length=20), nullable=True),
    sa.Column('text_border_size', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sponsor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sponsor_user_id', sa.Integer(), nullable=False),
    sa.Column('creator_user_id', sa.Integer(), nullable=False),
    sa.Column('tier_id', sa.Integer(), nullable=False),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['creator_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sponsor_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['tier_id'], ['sponsorship_tier.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sponsor_benefit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tier_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('delivery_method', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['tier_id'], ['sponsorship_tier.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sponsor_transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sponsor_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('transaction_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['sponsor_id'], ['sponsor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sponsor_transaction')
    op.drop_table('sponsor_benefit')
    op.drop_table('sponsor')
    op.drop_table('user_design')
    op.drop_table('sponsorship_tier')
    op.drop_table('flask_dance_oauth')
    op.drop_table('custom_field')
    op.drop_table('user')
    # ### end Alembic commands ###
