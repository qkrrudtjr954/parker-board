"""comments count to comment count

Revision ID: c4036ecdbefe
Revises: 5fa69d48f5ab
Create Date: 2018-07-06 10:55:37.488203

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c4036ecdbefe'
down_revision = '5fa69d48f5ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('comment_count', sa.Integer(), nullable=False))
    op.drop_column('post', 'comments_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('comments_count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_column('post', 'comment_count')
    # ### end Alembic commands ###
