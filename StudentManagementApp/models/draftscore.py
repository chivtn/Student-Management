from StudentManagementApp import db
from StudentManagementApp.models.enums import ScoreType

class DraftScore(db.Model):
    __tablename__ = 'draft_score'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    type = db.Column(db.Enum(ScoreType), nullable=False)
    value = db.Column(db.Float, nullable=False)

    student = db.relationship('Student', backref=db.backref('draft_scores', lazy=True))
    subject = db.relationship('Subject')
    semester = db.relationship('Semester')
