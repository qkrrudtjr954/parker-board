"""break off comment post relationship

Revision ID: ee58094a5a7c
Revises: db8e614d2509
Create Date: 2018-07-06 15:24:04.999525

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ee58094a5a7c'
down_revision = 'db8e614d2509'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('comment_ibfk_3', 'comment', type_='foreignkey')
    op.drop_column('comment', 'post_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('post_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.create_foreign_key('comment_ibfk_3', 'comment', 'post', ['post_id'], ['id'])
    # ### end Alembic commands ###
