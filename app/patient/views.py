from flask import render_template, url_for, flash, redirect, request, json, jsonify
from . import bp_patient
from .. import bcrypt
from .form import RegistrationForm, LoginForm, UpdateAccountForm
from ..model import Patient, MedicalStaff, Department, Bed, Ward, Reservation, db, Medicine, Prescription, Prescription_Detail, Schedule, Post
from flask_login import login_user, current_user, logout_user, login_required
import datetime

@bp_patient.route("/")
@bp_patient.route("/patient/homepage")
def homepage():
    notice = Post.query.all()
    return render_template('patient/pages-index.html',notice=notice)


@bp_patient.route("/patient/register", methods=['GET', 'POST'])
def patient_register():
    if current_user.is_authenticated:
        return redirect(url_for('patient.homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf=8')
        user = Patient(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('patient.patient_login'))
    return render_template('patient/pages-register.html', title='Register', form=form)


@bp_patient.route("/patient/login", methods=['GET', 'POST'])
def patient_login():
    if current_user.is_authenticated:
        return redirect(url_for('patient.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Patient.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('patient.homepage'))
        else:
            flash('Login Unsuccessful. Pleach check again', 'danger')
    return render_template('patient/pages-login.html', title='Login', form=form)


@bp_patient.route("/patient/logout")
def patient_logout():
    logout_user()
    return redirect(url_for('patient.homepage'))


@bp_patient.route("/patient/account", methods=['GET', 'POST'])
@login_required
def patient_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.gender = form.gender.data
        current_user.birthDay = form.birthDay.data
        current_user.phoneNumber = form.phoneNumber.data
        current_user.address = form.address.data
        db.session.commit()
        return redirect(url_for('patient.homepage'))
    elif request.method == 'GET':
        form.gender.data = current_user.gender
        form.birthDay.data = current_user.birthDay
        form.phoneNumber.data = current_user.phoneNumber
        form.address.data = current_user.address
    return render_template('patient/pages-profile.html', title='Account', form=form)

'''
@bp_patient.route("/patient/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('patient/pages-notice.html', title='Write a Notice', form=form, legend='Write a Notice')
'''


@bp_patient.route("/patient/doctorinfo", methods=['GET', 'POST'])
def doctorinfo():
    if request.method == "POST":
        if request.form['search_department'] == 'Ophthalmology':
            DoctorInfo = db.session.query(MedicalStaff.name,Department.departmentName,MedicalStaff.position,MedicalStaff.gender,
                                             MedicalStaff.officeNo).filter(MedicalStaff.department_ID == Department.department_ID,
                                                                           Department.departmentName == 'Ophthalmology',
                                                                           MedicalStaff.StaffID.like('D%')).all()

        elif request.form['search_department'] == 'Dermatology':
            DoctorInfo = db.session.query(MedicalStaff.name, Department.departmentName, MedicalStaff.position,MedicalStaff.gender,
                                             MedicalStaff.officeNo).filter(MedicalStaff.department_ID == Department.department_ID,
                                                                           Department.departmentName == 'Dermatology',
                                                                           MedicalStaff.StaffID.like('D%')).all()

        elif request.form['search_department'] == 'The whole Staff':
            DoctorInfo = db.session.query(MedicalStaff.name, Department.departmentName, MedicalStaff.position,MedicalStaff.gender,
                                          MedicalStaff.officeNo).filter(MedicalStaff.department_ID == Department.department_ID,
                                                                            MedicalStaff.StaffID.like('D%')).all()

        elif request.form['search_department'] == 'Internal medicine':
            DoctorInfo = db.session.query(MedicalStaff.name, Department.departmentName, MedicalStaff.position,MedicalStaff.gender,
                                          MedicalStaff.officeNo).filter(MedicalStaff.department_ID == Department.department_ID,
                                                                            Department.departmentName == 'Internal medicine',
                                                                            MedicalStaff.StaffID.like('D%')).all()

        elif request.form['search_department'] == 'Dentistry':
            DoctorInfo = db.session.query(MedicalStaff.name, Department.departmentName, MedicalStaff.position,MedicalStaff.gender,
                                          MedicalStaff.officeNo).filter(MedicalStaff.department_ID == Department.department_ID,
                                                                            Department.departmentName == 'Dentistry',
                                                                            MedicalStaff.StaffID.like('D%')).all()

        else:
            DoctorInfo = db.session.query(MedicalStaff.name, Department.departmentName, MedicalStaff.position,MedicalStaff.gender,
                                          MedicalStaff.officeNo).filter(MedicalStaff.department_ID == Department.department_ID,
                                                                            Department.departmentName == 'Surgery',
                                                                            MedicalStaff.StaffID.like('D%')).all()

        return render_template('patient/pages-doctorinfo.html', title='Doctor Information Center', DoctorInfo=DoctorInfo)

    DoctorInfo = db.session.query(MedicalStaff.name, Department.departmentName, MedicalStaff.position,MedicalStaff.gender,
                                  MedicalStaff.officeNo).filter(MedicalStaff.department_ID == Department.department_ID,
                                                                MedicalStaff.StaffID.like('D%')).all()

    return render_template('patient/pages-doctorinfo.html', title='Doctor Information Center', DoctorInfo=DoctorInfo)


@bp_patient.route("/patient/priceinfo", methods=['GET', 'POST'])
def priceinfo():
    if request.method == "POST":

        if request.form['search_price'] == 'Hospitalization Expenses':
            HopitalizationInfo = db.session.query(Ward.capacity, Bed.price).distinct().filter(Bed.ward_No == Ward.wardNo).order_by(Bed.price.desc()).all()
            return render_template('patient/pages-priceinfo.html', title='Price Information Center', HopitalizationInfo=HopitalizationInfo)

        if request.form['search_price'] == 'Medicine Price':
            MedicinePrice = db.session.query(Medicine.m_name, Medicine.price, Medicine.description).distinct().all()
            return render_template('patient/pages-priceinfo.html', title='Price Information Center', MedicinePrice=MedicinePrice)

    HopitalizationInfo = db.session.query(Ward.capacity, Bed.price).distinct().filter(Bed.ward_No == Ward.wardNo).order_by(Bed.price.desc()).all()
    return render_template('patient/pages-priceinfo.html', title='Price Information Center', HopitalizationInfo=HopitalizationInfo)




@bp_patient.route('/patient/reservation/doctor', methods=['GET', 'POST'])
def searchreservation():
    data = request.get_json()
    print(request.get_json())

    now_date = datetime.datetime.now()
    tomorrow_date = now_date + datetime.timedelta(days=1)
    print(tomorrow_date)

    schedule = Schedule.query.filter(Schedule.staff_ID==data['doctorid'], Schedule.date==tomorrow_date)

    return "ok"

@bp_patient.route('/patient/searchdoc', methods=['POST'])
def searchdoc():
    dname=request.form['search_department']
    print(dname)
    DoctorInfo = MedicalStaff.query.filter(MedicalStaff.department.departmentName==dname).all()
    return render_template('patient/pages-reservation.html', title='Doctor Information Center', DoctorInfo=DoctorInfo)

@bp_patient.route("/patient/reservation", methods=['GET', 'POST'])
def reservation():
    dt=datetime.datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        departmentname=request.form['search_department']
        print(departmentname)
        department=Department.query.filter(Department.departmentName==departmentname).first()
        if departmentname != 'All':
            schedules = Schedule.query.join(MedicalStaff).filter(MedicalStaff.department_ID == department.department_ID,
                                                                 Schedule.date > dt).all()
        else:
            schedules = Schedule.query.filter(Schedule.staff_ID.like('D%'), Schedule.date > dt).all()
        return render_template('patient/pages-reservation.html', title='Doctor Information Center', schedules=schedules)
        #redirect(url_for('patient.reservation',title='Doctor Information Center', schedules=schedules))

    schedules=Schedule.query.filter(Schedule.date > dt).all()
    #DoctorInfo = MedicalStaff.query.filter(MedicalStaff.StaffID.like('D%')).all()

    return render_template('patient/pages-reservation.html', title='Doctor Information Center',schedules=schedules)


@bp_patient.route("/patient/myreservation", methods=['GET', 'POST'])
@login_required
def myreservation():
    print("here")
    MyReservation = db.session.query(Reservation.reservationID, Department.departmentName, Reservation.doctor_ID, Patient.name, Reservation.reservationTime,
                                     Reservation.reservationDate, Reservation.description).filter(Reservation.doctor_ID == MedicalStaff.StaffID,
                                                                                                  Reservation.id == Patient.id,
                                                                                                  MedicalStaff.department_ID == Department.department_ID,
                                                                                                  Reservation.reservationDate > datetime.datetime.strftime(datetime.datetime.today(), '%y-%m-%d'),
                                                                                                  Reservation.doctor_ID.like('D%')).all()

    return render_template('patient/pages-myreservation.html', title='Check my reservation', MyReservation=MyReservation)


@bp_patient.route("/patient/reservationrecord", methods=['GET', 'POST'])
@login_required
def reservationrecord():

    MyOldReservation = db.session.query(Reservation.reservationID, Department.departmentName, Reservation.doctor_ID, Patient.name,
                                     Reservation.reservationDate, Reservation.description).filter(Reservation.doctor_ID == MedicalStaff.StaffID,
                                                                                                  Reservation.id == Patient.id,
                                                                                                  MedicalStaff.department_ID == Department.department_ID,
                                                                                                  Reservation.reservationDate < datetime.datetime.strftime(datetime.datetime.today(),'%y-%m-%d'),
                                                                                                  Reservation.doctor_ID.like('D%')).all()

    if request.method == "POST":
        print(request.form)
    return render_template('patient/pages-reservationrecord.html', title='Reservation History', MyOldReservation=MyOldReservation)


@bp_patient.route('/patient/myreservation_cancel', methods=['GET', 'POST'])
def myreservation_cancel():
    reservationID = request.args.get('reservationID')

    address = Reservation.query.filter_by(reservationID=reservationID).first()
    db.session.delete(address)
    db.session.commit()
    return redirect(url_for('patient.myreservation'))
    return render_template('patient/pages-myreservation.html', title='Check my reservation')


@bp_patient.route('/patient/medicineinfo')
def patient_medicine():
    MedicineInfo = db.session.query(Medicine.medicineID, Medicine.m_name, Medicine.price, Medicine.company, Medicine.description).all()

    return render_template('patient/pages-medicineinfo.html', title="Medicine Information Archive", MedicineInfo=MedicineInfo)


@bp_patient.route("/patient/prescriptiondetail")
def prescriptiondetail():
    prescription = db.session.query(Prescription.prescriptionID,Prescription.giveStatues,Prescription.paymentStatues,Patient.name).filter(Prescription.giveStatues == 'n',
                                                                                                                Prescription.id == Patient.id).all()
    prescription_detail = Prescription_Detail.query.all()
    if request.method == "POST":
        print(request.form)
    return render_template('patient/pages-prescriptiondetail.html', title ='Check my prescription', prescription=prescription, prescription_detail=prescription_detail)


@bp_patient.route('/patient/searchpre', methods=['GET', 'POST'])
def searchpre():
    data = request.get_json()
    print(request.get_json())
    prescription = Prescription_Detail.query.filter(Prescription_Detail.prescriptionID == data['pid']).all()
    medicinepre = {}
    i = 0
    for medicine in prescription:
        medicinepre[i] = medicine.to_json()
        i = i + 1
    print(medicinepre)
    print("here")
    return json.dumps(medicinepre)


@bp_patient.route("/patient/prescriptionrecord", methods=['GET', 'POST'])
@login_required
def prescriptionrecord():

    MyOldPrescription = db.session.query(Prescription.prescriptionID, Medicine.medicineID ,Medicine.m_name, Medicine.company, Medicine.price, Medicine.description , Prescription_Detail.quantity, Patient.name,
                                     Prescription.prescriptionDate).distinct().filter(Prescription.prescriptionID == Prescription_Detail.prescriptionID,Prescription_Detail.medicine_ID == Medicine.medicineID,
                                                                                                  Prescription.id == Patient.id,
                                                                                      Reservation.reservationDate > datetime.datetime.strftime(datetime.datetime.today(),'%y-%m-%d')).order_by(Prescription.prescriptionID.asc(),Medicine.medicineID.asc()).all()

    if request.method == "POST":
        print(request.form)
    return render_template('patient/pages-prescriptionrecord.html', title='Prescription History', MyOldPrescription=MyOldPrescription)

@bp_patient.route('/patient/givemedicine', methods=['GET', 'POST'])
def givemedicine():
    prescription = Prescription.query.filter(Prescription.giveStatues == 'n').all()
    if request.method == 'POST':
            print('here')
            pid = request.form['pid']
            print(pid)
            prescription1 = Prescription.query.filter(Prescription.prescriptionID == pid).first()
            prescription1.paymentStatues = 'y'
            db.session.commit()

            prescription = Prescription.query.filter(Prescription.giveStatues == 'n').all()
            #return render_template('patient/pages-prescriptiondetail.html', prescription=prescription)
            return  redirect(url_for('patient.prescriptiondetail'))

    return render_template('patient/pages-prescriptiondetail.html', prescription=prescription)

def makereservation():
    pass

@bp_patient.route('/patient/confirmReservation', methods=['GET', 'POST'])
def confirmReservation():
    print(request.form)
    patientID=request.form['patientID']
    doctorID = request.form['doctorID']
    confirm_date = request.form['confirm_date']
    confirm_time = request.form['confirm_time']

    tag = confirm_time[1]
    if tag == ':':
        time = confirm_time[0]
    else:
        time = confirm_time[0:2]
    db.session.add(Reservation(reservationID=createID(),doctor_ID=doctorID, id=patientID,
                                reservationDate=confirm_date, reservationTime=time))
    db.session.commit()


    return redirect(url_for("patient.reservation"))

def createID():
    reservationID = Reservation.query.order_by(
        Reservation.reservationID.desc()).first()
    if reservationID is None:
        return '00001'
    print(reservationID)
    id = reservationID.reservationID[:]

    for i in range(1, 1000):
        newid = ("{:0>4d}".format(i))
        if id == newid:
            newid = ("{:0>4d}".format(i + 1))
            break

    return newid