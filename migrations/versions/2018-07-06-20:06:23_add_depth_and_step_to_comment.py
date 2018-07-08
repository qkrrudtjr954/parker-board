"""add depth and step to comment

Revision ID: 9758751f8e81
Revises: 2c1df37a2e4e
Create Date: 2018-07-06 20:06:23.445170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9758751f8e81'
down_revision = '2c1df37a2e4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('depth', sa.Integer(), nullable=False))
    op.add_column('comment', sa.Column('step', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'step')
    op.drop_column('comment', 'depth')
    # ### end Alembic commands ###
