"""empty message

Revision ID: 56b39070bc4a
Revises: b3deab6435c9
Create Date: 2019-12-22 23:11:42.824582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56b39070bc4a'
down_revision = 'b3deab6435c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'hospitalization', 'bed', ['bedNo'], ['bedNo'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'hospitalization', type_='foreignkey')
    # ### end Alembic commands ###