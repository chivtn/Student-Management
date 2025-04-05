# models/teacher.py
from StudentManagementApp import db

class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

    subject = db.relationship('Subject', backref='teachers')
    user = db.relationship('User', backref='teacher_profile')
    classrooms = db.relationship('Classroom', secondary='teacher_classroom', back_populates='teachers')
    homeroom_class = db.relationship('Classroom', uselist=False, backref='homeroom_teacher', foreign_keys='Classroom.homeroom_teacher_id')

