#stat.service
import random
import hashlib
from sqlalchemy import func
from StudentManagementApp.models import *
from StudentManagementApp import app, db

# --- THỐNG KÊ ĐIỂM MÔN HỌC ---
def statistics_subject(classroom_id, subject_id, semester_id):
    students = Student.query.filter_by(classroom_id=classroom_id).all()
    scores = {}

    for student in students:
        scores[student.id] = {
            'id_student': student.id,
            'score': 0,
        }

    def query_score(score_type_label):
        return db.session.query(
            ScoreDetail.score_sheet_id,
            func.sum(ScoreDetail.value),
            func.count(ScoreDetail.value)
        ).join(ScoreSheet, ScoreSheet.id == ScoreDetail.score_sheet_id) \
            .filter(
            ScoreSheet.classroom_id == classroom_id,
            ScoreSheet.subject_id == subject_id,
            ScoreSheet.semester_id == semester_id,
            ScoreDetail.type == score_type_label
        ).group_by(ScoreDetail.score_sheet_id).all()

    test_15m = query_score(ScoreType.FIFTEEN_MIN)
    test_45m = query_score(ScoreType.ONE_PERIOD)
    test_final = query_score(ScoreType.FINAL)

    for i, (student_id, a_sum, a_count) in enumerate(test_15m):
        b_sum, b_count = (0, 0)
        c_sum, c_count = (0, 0)

        for sid, s, c in test_45m:
            if sid == student_id:
                b_sum, b_count = s, c
        for sid, s, c in test_final:
            if sid == student_id:
                c_sum, c_count = s, c

        if a_count + b_count*2 + c_count*3 > 0:
            final_score = (a_sum + b_sum*2 + c_sum*3) / (a_count + b_count*2 + c_count*3)
            scores[student_id]['score'] = round(final_score, 1)

    return scores

# --- THỐNG KÊ SỐ LƯỢNG ---
def count_users():
    return User.query.count()

def count_subjects():
    return Subject.query.count()

def count_classrooms():
    return Classroom.query.count()

def count_teachers():
    return User.query.filter_by(role=Role.TEACHER).count()

# --- AUTH ADMIN ---
def auth_admin(username, password):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    return User.query.filter_by(username=username, password=password, role=Role.ADMIN).first()
