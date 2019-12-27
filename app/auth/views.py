from flask import render_template, redirect, flash, request, session, url_for
# 导入表单处理方法
from werkzeug.security import check_password_hash, generate_password_hash

from . import bp_auth
from ..model import Patient, MedicalStaff, Department, db, Post


@bp_auth.route('/', methods=['GET', 'POST'])
def welcome():
    session.clear()
    connection = db.engine.raw_connection()
    cursor = connection.cursor()
    #cursor.execute('call doctor_popular()')
    cursor.execute('call doctor_top()')
    doctorlist=(cursor.fetchall())

    print(doctorlist)
    notice = Post.query.all()
    return render_template('mainpage.html',doctorlist=doctorlist,notice=notice)
    # return "ok"

    #return redirect(url_for('warehouse.homepage'))
    #return redirect(url_for('warehouse.prescription'))
    #return redirect(url_for('doctor.homepage'))
    #return redirect(url_for('doctor.homepageleader'))
    #return redirect(url_for('nurse.homepage'))

@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        userID = request.form["ID"]
        password = request.form["password"]
        print(userID)
        print(password)
        #whether it is hr/ administor
        if userID == 'admin' and password=='a':
            session.clear()
            session["user_id"] = userID
            return redirect(url_for('hr.homepage'))

        error = None
        error = check_user(userID, password)

        if error is None:
            # store the wechat id in a new session and return to the index
            session.clear()
            session["user_id"] = userID

            if userID[0] == 'D':
                return redirect(url_for('doctor.homepage', userid=userID))
            elif userID[0] == 'N':
                user = MedicalStaff.query.filter(MedicalStaff.StaffID == userID).first()
                if user.position=='Leader':
                    return redirect(url_for('nurse.homepageleader', userid=userID))
                else:
                    return redirect(url_for('nurse.homepage', userid=userID))
            elif userID[0] == 'W':
                return redirect(url_for('warehouse.homepage', userid=userID))
            else:
                return redirect(url_for('hr.homepage', userid=userID))


        flash(error)

    return render_template("auth/profile.html")


@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        error = None
        pName = request.form["name"]
        print(pName)
        password = request.form["password"]
        print(password)

        gender = request.form["gender"]
        print(gender)

        birthday = request.form["birthday"]
        print(birthday)

        phoneNumber = request.form["phonenumber"]
        print(phoneNumber)

        gender = 'm'

        if Patient.query.filter(Patient.phoneNumber == phoneNumber).first() is not None:
            error = "User {0} is already registered.".format(phoneNumber)

        # patientID = db.Column(db.CHAR(4), primary_key=True)  # 每个用户记得添加用户组
        # name = db.Column(db.CHAR(20))
        # gender = db.Column(db.CHAR(1))
        # birthDay = db.Column(db.DATE)
        # phoneNumber = db.Column(db.CHAR(11))
        # address = db.Column(db.CHAR(20))
        # password = db.Column(db.VARCHAR(100))
        if error is None:
            db.session.add(Patient(patientID='0002', phoneNumber=phoneNumber, password=generate_password_hash(password),
                           name=pName, gender=gender, birthDay=birthday))
            db.session.commit()
            redirect(url_for("auth.login"))
    return render_template('auth/register.html')


def check_user(userID, password):
    error = None
    if userID[0] == 'D' or userID[0] == 'N' or userID[0] == 'W' or userID[0] == 'H':
        user = MedicalStaff.query.filter(MedicalStaff.StaffID == userID).first()
        if user is None:
            error = "Incorrect username."
        elif user.password is None:
            error = "Incorrect password."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."
        return error
    else:
        user = Patient.query.filter(Patient.patientID == userID).first()
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        return error





        # print(patientID)
        # print(password)
        #
        # user = Patient.query.filter(Patient.patientID == patientID).first()
        #
        #
        # if user is None:
        #     error = "Incorrect username."
        #     print("Incorrect username.")
        # elif not check_password_hash(user.password, password):
        #     error = "Incorrect password."
        #     print("Incorrect password.")

