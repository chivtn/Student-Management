# models/teacher_classroom.py (many-to-many)
from StudentManagementApp import db

Teacher_Classroom = db.Table(
    'teacher_classroom',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'), primary_key=True),
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'), primary_key=True)
)