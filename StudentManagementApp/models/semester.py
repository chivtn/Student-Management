# models/semester.py
from StudentManagementApp import db

class Semester(db.Model):
    __tablename__ = 'semester'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)