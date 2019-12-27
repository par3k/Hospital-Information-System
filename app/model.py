# -*- coding: utf-8 -*-
from flask_login import UserMixin

from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):

    return Patient.query.get(user_id)

class Patient(db.Model, UserMixin):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.CHAR(20))
    gender = db.Column(db.CHAR(10))
    birthDay = db.Column(db.DATE)
    phoneNumber = db.Column(db.CHAR(50))
    email = db.Column(db.CHAR(120))
    address = db.Column(db.CHAR(20))
    password = db.Column(db.VARCHAR(100))

    hsprefer = db.relationship('Hspapply', backref='patient')
    postrefer = db.relationship('Post', backref='patient')
    reservationrefer = db.relationship('Reservation', backref='patient')
    prescriptionrefer = db.relationship('Prescription', backref='patient')
    hospitalizationrefer = db.relationship('Hospitalization', backref='patient')
    nursingrefer = db.relationship('Nursing', backref='patient')

class MedicalStaff(db.Model):
    __tablename__ = 'medicalstaff'
    StaffID = db.Column(db.CHAR(4), primary_key=True)
    name = db.Column(db.CHAR(20))
    gender = db.Column(db.CHAR(10))
    department_ID = db.Column(db.CHAR(3), db.ForeignKey('department.department_ID'), nullable=True)
    entryDay = db.Column(db.DATE)
    retirementDate = db.Column(db.DATE)
    phoneNumber = db.Column(db.CHAR(11))
    officeNo = db.Column(db.CHAR(10))
    position = db.Column(db.CHAR(20))
    email = db.Column(db.CHAR(20))
    salary = db.Column(db.Integer)
    password = db.Column(db.VARCHAR(100))
    status = db.Column(db.CHAR(20))

    hsprefer = db.relationship('Hspapply', backref='medicalstaff')
    postrefer = db.relationship('Post', backref='medicalstaff')
    warehouserefer = db.relationship('Warehouse', backref='medicalstaff')
    reservationrefer = db.relationship('Reservation', backref='medicalstaff')
    hospitalizationrefer = db.relationship('Hospitalization', backref='medicalstaff')
    prescriptionrefer = db.relationship('Prescription', backref='medicalstaff')
    nursingrefer = db.relationship('Nursing', backref='medicalstaff')
    schedualrefer = db.relationship('Schedule', backref='medicalstaff')
#
class Department(db.Model):
    __tablename__ = 'department'
    department_ID = db.Column(db.CHAR(3), primary_key=True)
    departmentName = db.Column(db.CHAR(30))
    doctor_ID = db.Column(db.CHAR(4), nullable=True)
    nurse_ID = db.Column(db.CHAR(4), nullable=True)

    wardrefer = db.relationship('Ward', backref='department')
    depart = db.relationship("MedicalStaff", backref="department")

class Medicine(db.Model):
    __tablename__ = 'medicine'
    medicineID = db.Column(db.CHAR(3), primary_key=True)
    m_name = db.Column(db.CHAR(20))
    company = db.Column(db.CHAR(20))
    price = db.Column(db.Integer)
    warehouse_ID = db.Column(db.CHAR(2), db.ForeignKey("warehouse.warehouseID"))
    inDate = db.Column(db.DATE)
    expireDate = db.Column(db.DATE)
    stock = db.Column(db.Integer)
    description = db.Column(db.VARCHAR(1000))

    prerefer = db.relationship('Prescription_Detail', backref='medicine')

    def to_json(self):
        json_medicine = {
            'medicineID': self.medicineID,
            'name': self.m_name,
            'company': self.company,
            'price': self.price,
            'warehouse_ID': self.warehouse_ID,
            'inDate': self.inDate.strftime('%Y-%m-%d'),
            'expireDate': self.expireDate.strftime('%Y-%m-%d'),
            'stock': self.stock,
            'description': self.description
        }
        return json_medicine

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    warehouseID=db.Column(db.CHAR(2), primary_key=True)
    warehouseadmin_ID = db.Column(db.CHAR(4), db.ForeignKey("medicalstaff.StaffID"))

    medicinerefer = db.relationship('Medicine', backref='warehouse')

class Reservation(db.Model):
    __tablename__ = 'reservation'
    reservationID = db.Column(db.CHAR(4), primary_key=True)
    doctor_ID = db.Column(db.CHAR(4), db.ForeignKey("medicalstaff.StaffID"))
    id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    reservationDate = db.Column(db.DATE)
    reservationTime = db.Column(db.CHAR(2))
    description = db.Column(db.VARCHAR(100))

class Prescription(db.Model):
    __tablename__ = 'prescription'
    prescriptionID = db.Column(db.CHAR(5), primary_key=True)
    doctor_ID = db.Column(db.CHAR(4), db.ForeignKey("medicalstaff.StaffID"))
    id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    prescriptionDate = db.Column(db.DATE)
    paymentStatues = db.Column(db.CHAR(1))
    giveStatues = db.Column(db.CHAR(1))

class Prescription_Detail(db.Model):
    __tablename__ = 'prescription_detail'
    prescriptionID = db.Column(db.CHAR(5), primary_key=True)
    medicine_ID = db.Column(db.CHAR(3),  db.ForeignKey("medicine.medicineID"), primary_key=True)
    quantity = db.Column(db.Integer)

    def to_json(self):
        json_prescription = {
            'mid':  self.medicine_ID,
            'name': self.medicine.m_name,
            'price': self.medicine.price,
            'quantity': self.quantity
        }
        return json_prescription


class Ward(db.Model):
    __tablename__ = 'ward'
    wardNo = db.Column(db.CHAR(10), primary_key=True, index=True)
    capacity = db.Column(db.Integer)
    department_ID = db.Column(db.CHAR(3), db.ForeignKey("department.department_ID"))
    bedrefer = db.relationship('Bed', backref='ward')

class Bed(db.Model):
    __tablename__ = 'bed'
    bedNo = db.Column(db.CHAR(4), primary_key=True)
    ward_No = db.Column(db.CHAR(10), db.ForeignKey("ward.wardNo"))
    price = db.Column(db.Integer)

    hospitalizationrefer = db.relationship('Hospitalization', backref='bed')

class Hospitalization(db.Model):
    __tablename__ = 'hospitalization'
    bedNo = db.Column(db.CHAR(4), db.ForeignKey("bed.bedNo"), nullable=True)
    id = db.Column(db.Integer, db.ForeignKey("patient.id"), primary_key=True)
    doctor_ID = db.Column(db.CHAR(4), db.ForeignKey("medicalstaff.StaffID"))
    nurse_ID = db.Column(db.CHAR(4))
    startDate = db.Column(db.DATE,primary_key=True)
    endDate = db.Column(db.DATE)
    transferHospital = db.Column(db.CHAR(50))

class Nursing(db.Model):
    __tablename__ = 'nursing'
    id = db.Column(db.Integer, db.ForeignKey("patient.id"), primary_key=True)
    nurseID = db.Column(db.CHAR(4), db.ForeignKey("medicalstaff.StaffID"), primary_key=True)
    date = db.Column(db.DATE, primary_key=True)
    conditionDesc = db.Column(db.VARCHAR(200))

    def to_json(self):
        json_condition = {
            'patientid':  self.id,
            'nurseid': self.nurseID,
            'date': self.date.strftime('%Y-%m-%d'),
            'condition': self.conditionDesc
        }
        return json_condition

class Schedule(db.Model):
    __tablename__ = 'schedule'
    staff_ID = db.Column(db.CHAR(4), db.ForeignKey("medicalstaff.StaffID"), primary_key=True)
    date = db.Column(db.DATE, primary_key=True)
    timeInterval8 = db.Column(db.CHAR(1))
    timeInterval9 = db.Column(db.CHAR(1))
    timeInterval10 = db.Column(db.CHAR(1))
    timeInterval11 = db.Column(db.CHAR(1))
    timeInterval14 = db.Column(db.CHAR(1))
    timeInterval15 = db.Column(db.CHAR(1))
    timeInterval16 = db.Column(db.CHAR(1))
    timeInterval17 = db.Column(db.CHAR(1))

class Hspapply(db.Model):
    __tablename__ = 'hspapply'
    hspid=db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    doctor_ID = db.Column(db.CHAR(4), db.ForeignKey("medicalstaff.StaffID"))
    applyDate = db.Column(db.DATE)
    arrangeStatus=db.Column(db.CHAR(1),default='n')

class Post(db.Model):
    __tablename__ = 'post'
    postid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_ID = db.Column(db.CHAR(4), db.ForeignKey("medicalstaff.StaffID"))
    id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=True)
    tostaff_ID = db.Column(db.CHAR(4))
    iaAll = db.Column(db.CHAR(1))
    postDate = db.Column(db.DATE)
    postContent = db.Column(db.CHAR(200))
    postTitle = db.Column(db.CHAR(100))


class Nurseschedule(db.Model):
    __tablename__ = 'nurseschedule'
    nurseID = db.Column(db.CHAR(4), db.ForeignKey("medicalstaff.StaffID"), primary_key=True)
    endDate = db.Column(db.DATE)
    startDate = db.Column((db.DATE), primary_key=True)

    def to_json(self):
        json_ns = {
            'nurseID':  self.nurseID,
            'endDate': self.endDate.strftime('%Y-%m-%d'),
            'startDate': self.startDate.strftime('%Y-%m-%d'),
        }
        return json_ns
