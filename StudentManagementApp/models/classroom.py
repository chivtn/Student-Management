# models/classroom.py
from StudentManagementApp import db
from StudentManagementApp.models.enums import Grade
from StudentManagementApp.models.teacher_classroom import Teacher_Classroom

class GradeLevel(db.Model):
    __tablename__ = 'gradelevel'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(Grade), nullable=False)

class Classroom(db.Model):
    __tablename__ = 'classroom'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gradelevel_id = db.Column(db.Integer, db.ForeignKey('gradelevel.id'), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    homeroom_teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), unique=True)

    gradelevel = db.relationship('GradeLevel', backref='classrooms')
    students = db.relationship('Student', backref='classroom')
    teachers = db.relationship('Teacher', secondary=Teacher_Classroom, back_populates='classrooms')