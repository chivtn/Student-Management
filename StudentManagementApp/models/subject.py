# models/subject.py
from StudentManagementApp import db

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gradelevel_id = db.Column(db.Integer, db.ForeignKey('gradelevel.id'))

    gradelevel = db.relationship('GradeLevel', backref='subjects')