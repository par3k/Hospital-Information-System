"""empty message

Revision ID: 17430108f6de
Revises: 861191fbf9ce
Create Date: 2019-12-21 16:10:48.963328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17430108f6de'
down_revision = '861191fbf9ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('postid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('staff_ID', sa.CHAR(length=4), nullable=True),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('tostaff_ID', sa.CHAR(length=4), nullable=True),
    sa.Column('iaAll', sa.CHAR(length=1), nullable=True),
    sa.Column('postDate', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['patient.id'], ),
    sa.ForeignKeyConstraint(['staff_ID'], ['medicalstaff.StaffID'], ),
    sa.ForeignKeyConstraint(['tostaff_ID'], ['medicalstaff.StaffID'], ),
    sa.PrimaryKeyConstraint('postid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###
