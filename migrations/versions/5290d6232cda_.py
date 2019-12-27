"""empty message

Revision ID: 5290d6232cda
Revises: 6b983e2d4d63
Create Date: 2019-12-24 21:46:10.664802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5290d6232cda'
down_revision = '6b983e2d4d63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('postTitle', sa.CHAR(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'postTitle')
    # ### end Alembic commands ###
