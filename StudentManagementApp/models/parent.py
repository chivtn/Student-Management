# models/parent.py
from StudentManagementApp import db
from StudentManagementApp.models.enums import Relationship

class Parent(db.Model):
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    relation = db.Column(db.Enum(Relationship))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    student = db.relationship('Student', backref='parent')