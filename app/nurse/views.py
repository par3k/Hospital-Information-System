from flask import render_template, request, redirect, url_for,session

from sqlalchemy import text
from werkzeug.security import generate_password_hash

from . import bp_nurse
from .. import db
from ..model import Schedule,Hospitalization,MedicalStaff,Department, Ward, Nursing, Bed, Nurseschedule, Post
import datetime

@bp_nurse.route('/nurse/homepage')
def homepage():
    notice = Post.query.all()
    nurseId=session["user_id"]
    inpatientList = db.session.query(Hospitalization).from_statement(
        text("SELECT * FROM hsp.hospitalization hos where hos.nurse_ID=:nurseId and hos.endDate is null ")). \
        params(nurseId=nurseId).all()
    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    return render_template('nurse/index.html',inpatientList=inpatientList,user=user,notice=notice)


@bp_nurse.route('/nurse/homepageLeader')
def homepageleader():
    notice = Post.query.all()
    department = Department.query.filter_by(nurse_ID=session["user_id"]).one().department_ID
    inpatientList = db.session.query(Hospitalization).from_statement(
        text("SELECT * FROM hsp.hospitalization hos where hos.doctor_ID in "
             "(select StaffID from hsp.medicalstaff where department_ID =:department) and hos.nurse_ID is NULL")). \
        params(department=department).all()
    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    return render_template('nurse/index_leader.html',inpatientList=inpatientList,user=user,notice=notice)

@bp_nurse.route('/nurse/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        officno = request.form['officeno']
        password = request.form['password']
        print("here")
        user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
        user.name = name
        user.phoneNumber = phone
        user.officeNo = officno
        if password != '':
            user.password = generate_password_hash(password)
        user.email = email
        db.session.commit()
        return redirect(url_for('nurse.profile'))

    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    print(user.name)
    return render_template('nurse/profile.html', user=user)


@bp_nurse.route('/nurse/addCondition/<data>', methods=['GET', 'POST'])
def addcondition(data):
    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    str=data.split(',')
    pId=str[0]
    pName=str[1]

    if request.method=="POST":
        print(request.form)
        date = request.form['record-date']
        condition = request.form['record-des']
        db.session.add(Nursing(id=pId, nurseID=session["user_id"], date=date,
                                    conditionDesc=condition))
        db.session.commit()

    nid=session["user_id"]
    conditionList=db.session.query(Nursing).from_statement(
        text("SELECT * FROM hsp.nursing n where n.id =:pId and n.nurseID=:nid")).\
        params(pId=pId,nid=nid).all()

    return render_template('nurse/addCondition.html',pId=pId,pName=pName,conditionList=conditionList,user=user)

# @bp_nurse.route('/nurse/addCondition/new', methods=['GET', 'POST'])
# def newcondition():
#     print(request.form)
#     newpId=pId
#     conditionList = db.session.query(Nursing).from_statement(
#         text("SELECT * FROM hsp.nursing n where n.id =:pId and n.nurseID='N001'")). \
#         params(pId=newpId).all()
#     return render_template('nurse/addCondition.html', pId=newpId, pName=pName, conditionList=conditionList)

@bp_nurse.route('/nurse/patientList', methods=['GET', 'POST'])
def patientlist():
    if request.method=="POST":
        data = request.get_json()
        print(data)
        bedInfo= Bed.query.filter_by(ward_No=data).all();
        beddict = {}
        i = 0
        for bed in bedInfo:
            beddict[i] = bed.to_json()
            i = i + 1
        return beddict


    department = Department.query.filter_by(nurse_ID=session["user_id"]).one().department_ID
    inpatientList=db.session.query(Hospitalization).from_statement(
        text("SELECT * FROM hsp.hospitalization hos where hos.doctor_ID in "
             "(select StaffID from hsp.medicalstaff where department_ID =:department)")).\
        params(department=department).all()

    wardList= Ward.query.filter_by(department_ID=department).all();
    bedList = db.session.query(Bed).from_statement(
        text("SELECT * FROM hsp.bed bed where bed.ward_No in "
             "(select wardNo from hsp.ward where department_ID =:department)")).\
        params(department=department).all()
    nurseList=db.session.query(MedicalStaff).from_statement(
        text("SELECT * FROM hsp.medicalstaff hos where StaffID like 'N%' and department_ID = :department ")).\
        params(department=department).all() #排班时间筛选

    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()

    return render_template('nurse/patientList.html',
                           inpatientList=inpatientList,wardList=wardList,nurseList=nurseList,bedList= bedList,user=user)

@bp_nurse.route('/nurse/patientList/register', methods=['GET', 'POST'])
def register():
    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    pId = request.form['reg-id']
    inDate = request.form['reg-inDate']
    bedNo = request.form['bedSelect']
    nurseId = request.form['nurseSelect']

    inpatient=Hospitalization.query.filter_by(id=pId, startDate=inDate).first()
    inpatient.nurse_ID=nurseId;
    inpatient.bedNo=bedNo
    db.session.commit()

    department = Department.query.filter_by(nurse_ID=session["user_id"]).one().department_ID
    inpatientList = db.session.query(Hospitalization).from_statement(
        text("SELECT * FROM hsp.hospitalization hos where hos.doctor_ID in "
             "(select StaffID from hsp.medicalstaff where department_ID =:department)")). \
        params(department=department).all()

    wardList = Ward.query.filter_by(department_ID=department).all();
    bedList = db.session.query(Bed).from_statement(
        text("SELECT * FROM hsp.bed bed where bed.ward_No in "
             "(select wardNo from hsp.ward where department_ID =:department)")). \
        params(department=department).all()
    nurseList = db.session.query(MedicalStaff).from_statement(
        text("SELECT * FROM hsp.medicalstaff hos where StaffID like 'N%' and department_ID = :department ")). \
        params(department=department).all()  # 排班时间筛选
    return render_template('nurse/patientList.html',
                           inpatientList=inpatientList, wardList=wardList, nurseList=nurseList, bedList=bedList,user=user)


@bp_nurse.route('/nurse/patientList/leave', methods=['GET', 'POST'])
def leave():
    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    pId = request.form['leave-id']
    inDate = request.form['leave-inDate']
    outDate = request.form['leave-outDate']
    transferHos = request.form['leave-trans']

    inpatient = Hospitalization.query.filter_by(id=pId, startDate=inDate).first()
    inpatient.endDate = outDate
    inpatient.transferHospital=transferHos
    db.session.commit()

    department = Department.query.filter_by(nurse_ID=session["user_id"]).one().department_ID
    inpatientList = db.session.query(Hospitalization).from_statement(
        text("SELECT * FROM hsp.hospitalization hos where hos.doctor_ID in "
             "(select StaffID from hsp.medicalstaff where department_ID =:department)")). \
        params(department=department).all()

    wardList = Ward.query.filter_by(department_ID=department).all();
    bedList = db.session.query(Bed).from_statement(
        text("SELECT * FROM hsp.bed bed where bed.ward_No in "
             "(select wardNo from hsp.ward where department_ID =:department)")). \
        params(department=department).all()
    nurseList = db.session.query(MedicalStaff).from_statement(
        text("SELECT * FROM hsp.medicalstaff hos where StaffID like 'N%' and department_ID = :department ")). \
        params(department=department).all()  # 排班时间筛选
    return render_template('nurse/patientList.html',
                           inpatientList=inpatientList, wardList=wardList, nurseList=nurseList, bedList=bedList,user=user)

@bp_nurse.route('/nurse/recordCondition')
def recordcondition():
    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    nurseId = session["user_id"]
    inpatientList = db.session.query(Hospitalization).from_statement(
        text("SELECT * FROM hsp.hospitalization hos where hos.nurse_ID=:nurseId and hos.endDate is null ")). \
        params(nurseId=nurseId).all()
    return render_template('nurse/recordCondition.html', inpatientList=inpatientList, user=user)

@bp_nurse.route('/nurse/getschedule',methods=['GET', 'POST'])
def getschedule():
    data = request.get_json()
    scheduleInfo = Nurseschedule.query.filter_by(nurseID=data).all()
    scheduledict = {}
    i = 0
    for schedule in scheduleInfo:
        scheduledict[i] = schedule.to_json()
        i = i + 1
    return scheduledict

@bp_nurse.route('/nurse/scheduleLeader',methods=['GET', 'POST'])
def scheduleleader():
    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    if request.method == "POST":
        data = request.get_json()
        nurseid = data['nurseId']
        data_from = data['data_from']
        data_to = data['data_to']
        print(data_from)

        i=0
        while i< len(data_from):
            nurseschedule = Nurseschedule.query.filter_by(nurseID=nurseid, startDate=data_from[i]).all()
            if len(nurseschedule) == 0:
                db.session.add(Nurseschedule(nurseID=nurseid, endDate=data_to[i], startDate=data_from[i]))
                db.session.commit()
            i=i+1

        #nurseschedule = Nurseschedule.query.filter_by(nurseID=nurseid, startDate=data_from[i]).all()
    department = Department.query.filter_by(nurse_ID=session["user_id"]).one().department_ID
    nurseInfo =db.session.query(MedicalStaff).from_statement(
        text("SELECT * FROM hsp.medicalstaff hos where StaffID like 'N%' and department_ID = :department ")).\
        params(department=department).all()
    return render_template('nurse/schedule_leader.html', nurseInfo=nurseInfo, user=user)


@bp_nurse.route('/nurse/schedule')
def schedule():
    # now = datetime.datetime.now()
    # delta = datetime.timedelta(days=7)
    # n_days = now + delta
    # scheduleInfo=Schedule.query.filter(db.cast(Schedule.date, db.DATE) >= db.cast(datetime.datetime.now(), db.DATE),
    #                                    db.cast(Schedule.date, db.DATE) <= db.cast(n_days, db.DATE)Schedule.staff_ID="N001").all()

    scheduleInfo=Nurseschedule.query.filter_by(nurseID=session["user_id"]).all()
    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    return render_template('nurse/schedule.html', scheduleInfo=scheduleInfo,user=user)


