# models/student.py
from StudentManagementApp import db
from StudentManagementApp.models.enums import Gender

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum(Gender))
    birth_date = db.Column(db.Date)
    address = db.Column(db.String(255))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))