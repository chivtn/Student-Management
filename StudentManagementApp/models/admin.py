# models/admin.py
from StudentManagementApp import db

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    user = db.relationship('User', backref='admin_profile')
