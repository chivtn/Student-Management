# models/regulation.py
from StudentManagementApp import db

class Regulation(db.Model):
    __tablename__ = 'regulation'
    id = db.Column(db.Integer, primary_key=True)
    min_age = db.Column(db.Integer, default=15)
    max_age = db.Column(db.Integer, default=20)
    max_class_size = db.Column(db.Integer, default=40)