# models/staff.py
from StudentManagementApp import db

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    user = db.relationship('User', backref='staff_profile')