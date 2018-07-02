"""fix readcount to read_count

Revision ID: 7b0ea160a84c
Revises: 2a959c929605
Create Date: 2018-07-02 14:09:29.633076

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7b0ea160a84c'
down_revision = '2a959c929605'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('read_count', sa.Integer(), nullable=False))
    op.alter_column('post', 'readcount',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'readcount',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.drop_column('post', 'read_count')
    # ### end Alembic commands ###
