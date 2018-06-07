"""test

Revision ID: a08e5ae7b3b6
Revises: fcbc530289f3
Create Date: 2018-06-07 15:32:59.132280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a08e5ae7b3b6'
down_revision = 'fcbc530289f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('description', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'description')
    # ### end Alembic commands ###
