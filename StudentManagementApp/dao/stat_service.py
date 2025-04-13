#stat_service.py
import random
import hashlib
from sqlalchemy import func
from StudentManagementApp.models import *
from StudentManagementApp import app, db
from StudentManagementApp.dao import staff_service as dao

# --- THỐNG KÊ ĐIỂM MÔN HỌC ---
def statistics_subject(classroom_id, subject_id, semester_id):
    students = dao.get_student_by_class(classroom_id)
    scores = {}

    for student in students:
        scores[student.id] = {"id_student": student.id, "score": 0}

    def query_scores(score_type):
        return db.session.query(
            ScoreSheet.student_id,
            func.sum(ScoreDetail.value),
            func.count(ScoreDetail.value)
        ).join(ScoreDetail, ScoreSheet.id == ScoreDetail.score_sheet_id) \
        .filter(
            ScoreSheet.classroom_id == classroom_id,
            ScoreSheet.subject_id == subject_id,
            ScoreSheet.semester_id == semester_id,
            ScoreDetail.type == score_type
        ).group_by(ScoreSheet.student_id).all()

    fifteen_scores = query_scores(ScoreType.FIFTEEN_MIN)
    one_period_scores = query_scores(ScoreType.ONE_PERIOD)
    final_scores = query_scores(ScoreType.FINAL)

    for sid, a_sum, a_count in fifteen_scores:
        b_sum, b_count = (0, 0)
        c_sum, c_count = (0, 0)

        for sid_b, s_b, c_b in one_period_scores:
            if sid_b == sid:
                b_sum, b_count = s_b, c_b
        for sid_c, s_c, c_c in final_scores:
            if sid_c == sid:
                c_sum, c_count = s_c, c_c

        total_weight = a_count + b_count * 2 + c_count * 3
        if total_weight > 0:
            avg = (a_sum + b_sum * 2 + c_sum * 3) / total_weight
            if sid in scores:
                scores[sid]['score'] = round(avg, 1)

    return list(scores.values())

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
