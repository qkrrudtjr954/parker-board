"""add post

Revision ID: 49388be3ab36
Revises: e422a89d03cc
Create Date: 2018-05-28 18:18:41.609605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49388be3ab36'
down_revision = 'e422a89d03cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('content', sa.String(length=2000), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###