import datetime
from flask import render_template, request, redirect, url_for, session, json, jsonify
from werkzeug.security import generate_password_hash

from . import bp_warehouse
from ..model import MedicalStaff, Department, db, Medicine, Prescription, Prescription_Detail, Post


@bp_warehouse.route('/warehouse/homoepage', methods=['GET', 'POST'])
def homepage():
    notice = Post.query.all()
    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    return render_template('warehouse/index.html', user=user, notice=notice)



@bp_warehouse.route('/warehouse/medicineinfo', methods=['GET', 'POST'])
def medicine():
    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    dt=datetime.date.today()
    if request.method == "POST":
        print(request.form)
        if request.form['formtype'] == 'search':
            name = request.form['search_name']
            department = request.form['search_department']
            status = request.form['search_status']
            print(name)
            print(department)
            print(status)
            '''
            这搜索页面我真的是······
            '''
            if name == '' and department == 'All' and status == 'All':
                staffInfo = MedicalStaff.query.all()
                print("1")
            elif name == '' and department == 'All' and status != 'All':
                staffInfo = MedicalStaff.query.filter(MedicalStaff.status == status).all()
                print("2")
            elif name == '' and department != 'All' and status == 'All':
                departmentid = Department.query.filter(Department.departmentName.like(department)).first().departmentID
                staffInfo = MedicalStaff.query.filter(MedicalStaff.department_ID == departmentid).all()
                print("3")
            elif name == '' and department != 'All' and status != 'All':
                departmentid = Department.query.filter(Department.departmentName.like(department)).first().departmentID
                staffInfo = MedicalStaff.query.filter(MedicalStaff.department_ID == departmentid, MedicalStaff.status ==
                                                      status).all()
                print("4")
            elif name != '' and department == 'All' and status == 'All':
                staffInfo = MedicalStaff.query.filter(MedicalStaff.name.like('%' + name + '%')).all()
                print("5")
            elif name != '' and department == 'All' and status != 'All':
                staffInfo = MedicalStaff.query.filter(MedicalStaff.name.like(name), MedicalStaff.status == status).all()
                print("6")
            elif name != '' and department != 'All' and status == 'All':
                departmentid = Department.query.filter(Department.departmentName.like(department)).first().departmentID
                staffInfo = MedicalStaff.query.filter(MedicalStaff.name.like(name), MedicalStaff.department_ID ==
                                                      departmentid).all()
                print("7")
            elif name != '' and department != 'All' and status != 'All':
                departmentid = Department.query.filter(Department.departmentName.like(department)).first().departmentID
                staffInfo = MedicalStaff.query.filter(MedicalStaff.name.like(name), MedicalStaff.department_ID ==
                                                      departmentid, MedicalStaff.status == status).all()
                print("8")
            else:
                pass
            print("9")
            # return redirect(url_for('hr.account', staffInfo=staffInfo))
            return render_template('hrAdmin/accountManage.html', staffInfo=staffInfo)
            print("10")

        elif request.form['formtype'] == 'modify':

            id = request.form['modify_id']

            name = request.form['modify_medicinename']
            price = request.form['modify_medicineprice']
            company = request.form['modify_medicinecompany']
            description = request.form['modify_medicinedescription']
            warehouse = request.form['modify_warehouse']
            stock = request.form['modify_stock']
            indate = request.form['modify_medicineindate']
            expiredate = request.form['modify_medicineexpiredate']

            medicine = Medicine.query.filter(Medicine.medicineID == id).first()

            medicine.name = name
            medicine.price = price
            medicine.company = company
            medicine.description = description
            medicine.warehouse_ID = warehouse
            medicine.stock = stock
            medicine.inDate = indate
            medicine.expireDate = expiredate
            db.session.commit()

        else:  # is formtype==add
            print('here')
            mid = createID()
            name = request.form['add_medicinename']
            price = request.form['add_medicineprice']
            company = request.form['add_medicinecompany']
            warehouse = request.form['add_warehouse']
            stock = request.form['add_stock']
            expiredate = request.form['add_medicineexpiredate']
            description = request.form['add_medicinedescription']
            indate = datetime.datetime.now().strftime("%Y-%m-%d")

            db.session.add(Medicine(medicineID=mid, m_name=name, company=company, price=price,
                                    warehouse_ID=warehouse, inDate=indate, expireDate=expiredate,
                                    description=description, stock=stock))
            db.session.commit()

        MedicineInfo = Medicine.query.all()
        return redirect(url_for('warehouse.medicine', staffInfo=MedicineInfo, user=user, dt=dt))

    medicineInfo = Medicine.query.all()
    return render_template('warehouse/medicineInfo.html', medicineInfo=medicineInfo, user=user, dt=dt)


@bp_warehouse.route('/warehouse/prescription', methods=['GET', 'POST'])
def prescription():
    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    prescription = Prescription.query.filter(Prescription.giveStatues == 'n').all()
    #prescription = Prescription.query.all()
    #print(prescription)
    prescription_detail = Prescription_Detail.query.all()
    if request.method == "POST":
        print(request.form)
        if request.form['formtype'] == 'search':
            name = request.form['search_name']
            department = request.form['search_department']
            status = request.form['search_status']

    return render_template('warehouse/prescription.html', prescription=prescription,
                           prescription_detail=prescription_detail,
                           user=user)


@bp_warehouse.route('/warehouse/profile', methods=['GET', 'POST'])
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
        return redirect(url_for('warehouse.profile'))

    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    return render_template('warehouse/profile.html', profile=user, user=user)


@bp_warehouse.route('/warehouse/search', methods=['GET', 'POST'])
def search():
    data = request.get_json()
    print(request.get_json())
    medicineInfo = Medicine.query.filter(Medicine.m_name.like('%' + data['name'] + '%')).all()


    medicinedict = {}
    i = 0
    print(medicineInfo)
    for medicine in medicineInfo:
        print('1')
        medicinedict[i] = medicine.to_json()
        i = i + 1

    print(medicinedict)
    print(jsonify(medicinedict))
    return medicinedict

@bp_warehouse.route('/warehouse/searchpre', methods=['GET', 'POST'])
def searchpre():
    data = request.get_json()
    print(request.get_json())
    prescription = Prescription_Detail.query.filter(Prescription_Detail.prescriptionID == data['pid']).all()

    medicinedict = {}
    i = 0
    print(prescription)
    for medicine in prescription:
        medicinedict[i] = medicine.to_json()
        i = i + 1

    return medicinedict


@bp_warehouse.route('/warehouse/givemedicine', methods=['GET', 'POST'])
def givemedicine():
    prescription = Prescription.query.filter(Prescription.giveStatues == 'n').all()
    user = MedicalStaff.query.filter(MedicalStaff.StaffID == session["user_id"]).first()
    if request.method == 'POST':
            print('here')
            pid = request.form['pid']
            print(pid)
            prescription1 = Prescription.query.filter(Prescription.prescriptionID == pid).first()
            prescription1.giveStatues = 'y'
            db.session.commit()

            prescription = Prescription.query.filter(Prescription.giveStatues == 'n').all()
            return render_template('warehouse/prescription.html', prescription=prescription,user=user)

    return render_template('warehouse/prescription.html', prescription=prescription, user=user)

def createID():
    medicineID = Medicine.query.order_by(
        Medicine.medicineID.desc()).first()
    if medicineID is None:
        return 'M01'

    id = medicineID.medicineID[1:]
    for i in range(1, 100):
        newid = ("{:0>2d}".format(i))
        if id == newid:
            newid = ("{:0>2d}".format(i + 1))
            break

    return 'M' + newid
    # for staff in staffID:
    #     print(staff.StaffID)

    # staffID1=MedicalStaff.query.filter(MedicalStaff.StaffID.like('D%')).order_by(MedicalStaff.StaffID.asc()).all()
    #
    # for staff in staffID1:
    #     print(staff.StaffID)
