"""init

Revision ID: 898869023d95
Revises: 
Create Date: 2019-01-13 17:13:56.365965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '898869023d95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('checkclass',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('checkcname', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('examclass',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('examname', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fdarea',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('Areaname', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fdworkarea',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('FDid', sa.String(length=64), nullable=True),
    sa.Column('FDareaid', sa.String(length=64), nullable=True),
    sa.Column('FDareaname', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fpinfo',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('FPname', sa.String(length=64), nullable=True),
    sa.Column('FPage', sa.Integer(), nullable=True),
    sa.Column('FPsex', sa.String(length=64), nullable=True),
    sa.Column('FPphone', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fptestresult',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('FPid', sa.String(length=64), nullable=True),
    sa.Column('FPname', sa.String(length=64), nullable=True),
    sa.Column('FPheartrate', sa.Integer(), nullable=True),
    sa.Column('FPbloodpressure', sa.Integer(), nullable=True),
    sa.Column('FPresultdate', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hospitalconstuct',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('inhospitalarea',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('areaname', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lectureplace',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('LPname', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('medicine',
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('medicineclass', sa.Integer(), nullable=True),
    sa.Column('medicinename', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patientinfo',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('birth', sa.Date(), nullable=True),
    sa.Column('sex', sa.Integer(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('price',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('optionid', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('specialconcern',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('SCpid', sa.String(length=64), nullable=True),
    sa.Column('SCpname', sa.String(length=64), nullable=True),
    sa.Column('SCpdate', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usergroup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bedinfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('areaid', sa.Integer(), nullable=True),
    sa.Column('isused', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['areaid'], ['inhospitalarea.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('checkitem',
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('checkitemname', sa.String(length=64), nullable=True),
    sa.Column('itemclass', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['itemclass'], ['checkclass.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('examitem',
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('examitemname', sa.String(length=64), nullable=True),
    sa.Column('itemclass', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['itemclass'], ['examclass.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hospitalclass',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('cid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cid'], ['hospitalconstuct.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('lecturetime',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('FDid', sa.String(length=64), nullable=True),
    sa.Column('LPid', sa.String(length=64), nullable=True),
    sa.Column('LPname', sa.String(length=64), nullable=True),
    sa.Column('LPdate', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['LPid'], ['lectureplace.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userinfo',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('sex', sa.Integer(), nullable=True),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('password', sa.String(length=64), nullable=True),
    sa.Column('groupid', sa.Integer(), nullable=True),
    sa.Column('ismenzhen', sa.Boolean(), nullable=True),
    sa.Column('iszhuyuan', sa.Boolean(), nullable=True),
    sa.Column('isjiating', sa.Boolean(), nullable=True),
    sa.Column('isjizhen', sa.Boolean(), nullable=True),
    sa.Column('isshoufei', sa.Boolean(), nullable=True),
    sa.Column('isguahao', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['groupid'], ['usergroup.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('doctortimetable',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('doctorid', sa.String(length=64), nullable=True),
    sa.Column('doctortime', sa.Integer(), nullable=True),
    sa.Column('cid', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['cid'], ['hospitalclass.id'], ),
    sa.ForeignKeyConstraint(['doctorid'], ['userinfo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expertstimetable',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userinfoid', sa.String(length=64), nullable=True),
    sa.Column('cid', sa.String(length=64), nullable=True),
    sa.Column('date', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cid'], ['hospitalclass.id'], ),
    sa.ForeignKeyConstraint(['userinfoid'], ['userinfo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fd',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('FDdoctorid', sa.String(length=64), nullable=True),
    sa.Column('FDdoctorname', sa.String(length=64), nullable=True),
    sa.Column('FDdoctorrank', sa.Integer(), nullable=True),
    sa.Column('FDdate', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['FDdoctorid'], ['userinfo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('imgdoctortimetable',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('doctorid', sa.String(length=64), nullable=True),
    sa.Column('doctortime', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['doctorid'], ['userinfo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('imgpcheckin',
    sa.Column('imgpcheckinid', sa.Integer(), nullable=False),
    sa.Column('patientid', sa.String(length=64), nullable=True),
    sa.Column('doctorid', sa.String(length=20), nullable=True),
    sa.Column('doctortype', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['doctorid'], ['userinfo.id'], ),
    sa.ForeignKeyConstraint(['patientid'], ['patientinfo.id'], ),
    sa.PrimaryKeyConstraint('imgpcheckinid')
    )
    op.create_table('opcheckin',
    sa.Column('opcheckinid', sa.Integer(), nullable=False),
    sa.Column('patientid', sa.String(length=64), nullable=True),
    sa.Column('doctorid', sa.String(length=20), nullable=True),
    sa.Column('doctortype', sa.Integer(), nullable=True),
    sa.Column('jips', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['doctorid'], ['userinfo.id'], ),
    sa.ForeignKeyConstraint(['patientid'], ['patientinfo.id'], ),
    sa.PrimaryKeyConstraint('opcheckinid')
    )
    op.create_table('imgpcheckinafford',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('imgpcheckinid', sa.Integer(), nullable=True),
    sa.Column('imgpid', sa.String(length=64), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['imgpcheckinid'], ['imgpcheckin.imgpcheckinid'], ),
    sa.ForeignKeyConstraint(['imgpid'], ['imgpcheckin.patientid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('imgpcost',
    sa.Column('imgpcheckinid', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['imgpcheckinid'], ['imgpcheckin.imgpcheckinid'], ),
    sa.PrimaryKeyConstraint('imgpcheckinid')
    )
    op.create_table('imgprecipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('imgpcheckinid', sa.Integer(), nullable=True),
    sa.Column('imgpid', sa.String(length=64), nullable=True),
    sa.Column('medicinenames', sa.String(length=128), nullable=True),
    sa.Column('medicinenumbers', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['imgpcheckinid'], ['imgpcheckin.imgpcheckinid'], ),
    sa.ForeignKeyConstraint(['imgpid'], ['imgpcheckin.patientid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('imgprecipeafford',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('imgpcheckinid', sa.Integer(), nullable=True),
    sa.Column('imgpid', sa.String(length=64), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['imgpcheckinid'], ['imgpcheckin.imgpcheckinid'], ),
    sa.ForeignKeyConstraint(['imgpid'], ['imgpcheckin.patientid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inpatientdeposit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patientid', sa.String(length=64), nullable=False),
    sa.Column('rest', sa.Float(), nullable=True),
    sa.Column('totalcost', sa.Float(), nullable=True),
    sa.Column('ischeck', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['opcheckin.opcheckinid'], ),
    sa.ForeignKeyConstraint(['patientid'], ['patientinfo.id'], ),
    sa.PrimaryKeyConstraint('id', 'patientid')
    )
    op.create_table('opcheck',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('opcheckinid', sa.Integer(), nullable=True),
    sa.Column('opid', sa.String(length=64), nullable=True),
    sa.Column('checkitems', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['opcheckinid'], ['opcheckin.opcheckinid'], ),
    sa.ForeignKeyConstraint(['opid'], ['opcheckin.patientid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('opcheckafford',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('opcheckinid', sa.Integer(), nullable=True),
    sa.Column('opid', sa.String(length=64), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['opcheckinid'], ['opcheckin.opcheckinid'], ),
    sa.ForeignKeyConstraint(['opid'], ['opcheckin.patientid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('opcheckinafford',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('opcheckinid', sa.Integer(), nullable=True),
    sa.Column('opid', sa.String(length=64), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['opcheckinid'], ['opcheckin.opcheckinid'], ),
    sa.ForeignKeyConstraint(['opid'], ['opcheckin.patientid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('opcost',
    sa.Column('opcheckinid', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['opcheckinid'], ['opcheckin.opcheckinid'], ),
    sa.PrimaryKeyConstraint('opcheckinid')
    )
    op.create_table('opexam',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('opcheckinid', sa.Integer(), nullable=True),
    sa.Column('opid', sa.String(length=64), nullable=True),
    sa.Column('examitems', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['opcheckinid'], ['opcheckin.opcheckinid'], ),
    sa.ForeignKeyConstraint(['opid'], ['opcheckin.patientid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('opexamafford',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('opcheckinid', sa.Integer(), nullable=True),
    sa.Column('opid', sa.String(length=64), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['opcheckinid'], ['opcheckin.opcheckinid'], ),
    sa.ForeignKeyConstraint(['opid'], ['opcheckin.patientid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oprecipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('opcheckinid', sa.Integer(), nullable=True),
    sa.Column('opid', sa.String(length=64), nullable=True),
    sa.Column('medicinenames', sa.String(length=128), nullable=True),
    sa.Column('medicinenumbers', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['opcheckinid'], ['opcheckin.opcheckinid'], ),
    sa.ForeignKeyConstraint(['opid'], ['opcheckin.patientid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oprecipeafford',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('opcheckinid', sa.Integer(), nullable=True),
    sa.Column('opid', sa.String(length=64), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['opcheckinid'], ['opcheckin.opcheckinid'], ),
    sa.ForeignKeyConstraint(['opid'], ['opcheckin.patientid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inpatienttableset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inpatienttimeandbedid', sa.String(length=128), nullable=True),
    sa.Column('inpatientcheckid', sa.String(length=128), nullable=True),
    sa.Column('inpatientinspectid', sa.String(length=128), nullable=True),
    sa.Column('inpatientprescriptid', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['inpatientdeposit.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inpatientcheck',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tableid', sa.Integer(), nullable=True),
    sa.Column('checkitemsid', sa.String(length=128), nullable=True),
    sa.Column('doctorinfoid', sa.String(length=64), nullable=True),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['doctorinfoid'], ['userinfo.id'], ),
    sa.ForeignKeyConstraint(['tableid'], ['inpatienttableset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inpatientinspect',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tableid', sa.Integer(), nullable=True),
    sa.Column('inspectitemsid', sa.String(length=128), nullable=True),
    sa.Column('doctorinfoid', sa.String(length=64), nullable=True),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['doctorinfoid'], ['userinfo.id'], ),
    sa.ForeignKeyConstraint(['tableid'], ['inpatienttableset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inpatientprescript',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tableid', sa.Integer(), nullable=True),
    sa.Column('medicineid', sa.String(length=128), nullable=True),
    sa.Column('medicinenumbers', sa.String(length=128), nullable=True),
    sa.Column('doctorinfoid', sa.String(length=64), nullable=True),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['doctorinfoid'], ['userinfo.id'], ),
    sa.ForeignKeyConstraint(['tableid'], ['inpatienttableset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inpatienttimeandbed',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tableid', sa.Integer(), nullable=True),
    sa.Column('bedid', sa.Integer(), nullable=True),
    sa.Column('doctorinfoid', sa.String(length=64), nullable=True),
    sa.Column('startdate', sa.Date(), nullable=True),
    sa.Column('enddate', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['bedid'], ['bedinfo.id'], ),
    sa.ForeignKeyConstraint(['doctorinfoid'], ['userinfo.id'], ),
    sa.ForeignKeyConstraint(['tableid'], ['inpatienttableset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inpatienttimeandbed')
    op.drop_table('inpatientprescript')
    op.drop_table('inpatientinspect')
    op.drop_table('inpatientcheck')
    op.drop_table('inpatienttableset')
    op.drop_table('oprecipeafford')
    op.drop_table('oprecipe')
    op.drop_table('opexamafford')
    op.drop_table('opexam')
    op.drop_table('opcost')
    op.drop_table('opcheckinafford')
    op.drop_table('opcheckafford')
    op.drop_table('opcheck')
    op.drop_table('inpatientdeposit')
    op.drop_table('imgprecipeafford')
    op.drop_table('imgprecipe')
    op.drop_table('imgpcost')
    op.drop_table('imgpcheckinafford')
    op.drop_table('opcheckin')
    op.drop_table('imgpcheckin')
    op.drop_table('imgdoctortimetable')
    op.drop_table('fd')
    op.drop_table('expertstimetable')
    op.drop_table('doctortimetable')
    op.drop_table('userinfo')
    op.drop_table('lecturetime')
    op.drop_table('hospitalclass')
    op.drop_table('examitem')
    op.drop_table('checkitem')
    op.drop_table('bedinfo')
    op.drop_table('usergroup')
    op.drop_table('specialconcern')
    op.drop_table('price')
    op.drop_table('patientinfo')
    op.drop_table('medicine')
    op.drop_table('lectureplace')
    op.drop_table('inhospitalarea')
    op.drop_table('hospitalconstuct')
    op.drop_table('fptestresult')
    op.drop_table('fpinfo')
    op.drop_table('fdworkarea')
    op.drop_table('fdarea')
    op.drop_table('examclass')
    op.drop_table('checkclass')
    # ### end Alembic commands ###
