# models/score_sheet.py
from StudentManagementApp import db

class ScoreSheet(db.Model):
    __tablename__ = 'score_sheet'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)

    student = db.relationship('Student', backref='score_sheets')
    subject = db.relationship('Subject', backref='score_sheets')
    semester = db.relationship('Semester', backref='score_sheets')