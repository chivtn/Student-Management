#score_service.py
from StudentManagementApp import db
from StudentManagementApp.models import ScoreSheet, ScoreDetail, DraftScore, ScoreType, Subject, Student
import re

def get_score_limits(subject_id):
    subject = Subject.query.get(subject_id)
    if subject:
        return subject.score15P_column_number or 0, subject.score1T_column_number or 0
    return 0, 0

def fetch_scores_for_students(students, academic_year_id, semester_id, subject_id):
    scores_map = {}
    for student in students:
        official = get_score_sheet(student.id, subject_id, semester_id, academic_year_id)
        draft = DraftScore.query.filter_by(
            student_id=student.id,
            subject_id=subject_id,
            semester_id=semester_id,
            academic_year_id=academic_year_id
        ).all()
        scores_map[student.id] = parse_combined_scores(official, draft)
    return scores_map

def get_score_sheet(student_id, subject_id, semester_id, academic_year_id):
    return ScoreSheet.query.filter_by(
        student_id=student_id,
        subject_id=subject_id,
        semester_id=semester_id,
        academic_year_id=academic_year_id
    ).first()

def parse_combined_scores(sheet, drafts):
    data = {
        "score_15": [],
        "score_1tiet": [],
        "score_final": None,
        "avg": None,
    }
    official_15 = []
    official_1t = []
    official_final = None

    if sheet:
        for detail in sheet.details:
            if detail.type == ScoreType.FIFTEEN_MIN:
                official_15.append(detail.value)
                data["score_15"].append({"value": detail.value, "readonly": True})
            elif detail.type == ScoreType.ONE_PERIOD:
                official_1t.append(detail.value)
                data["score_1tiet"].append({"value": detail.value, "readonly": True})
            elif detail.type == ScoreType.FINAL:
                official_final = detail.value
                data["score_final"] = {"value": detail.value, "readonly": True}

    for d in drafts:
        if d.type == ScoreType.FIFTEEN_MIN and d.value not in official_15:
            data["score_15"].append({"value": d.value, "readonly": False})
        elif d.type == ScoreType.ONE_PERIOD and d.value not in official_1t:
            data["score_1tiet"].append({"value": d.value, "readonly": False})
        elif d.type == ScoreType.FINAL and official_final is None:
            data["score_final"] = {"value": d.value, "readonly": False}

    s15 = [x["value"] for x in data["score_15"]]
    s1t = [x["value"] for x in data["score_1tiet"]]
    final = data["score_final"]["value"] if data["score_final"] else None
    if s15 and s1t and final is not None:
        data["avg"] = compute_weighted_average(s15, s1t, final)

    return data

def compute_weighted_average(s15, s1t, final):
    avg_15 = sum(s15) / len(s15)
    avg_1t = sum(s1t) / len(s1t)
    return round((avg_15 * 1 + avg_1t * 2 + final * 3) / 6, 2)

def store_scores(form_data, students, academic_year_id, semester_id, subject_id):
    for student in students:
        sheet = get_or_create_score_sheet(student.id, subject_id, semester_id, academic_year_id)
        save_score_details(sheet, form_data, student.id)
        delete_draft_scores(student.id, subject_id, semester_id, academic_year_id)
    db.session.commit()

def save_draft_scores(form_data, students, academic_year_id, semester_id, subject_id):
    for student in students:
        DraftScore.query.filter_by(
            student_id=student.id,
            subject_id=subject_id,
            semester_id=semester_id,
            academic_year_id=academic_year_id
        ).delete()

        draft_scores = []
        max_15, max_1t = get_score_limits(subject_id)
        draft_scores.extend(extract_unique_scores(
            form_data, student.id, subject_id, semester_id, academic_year_id,
            '15', ScoreType.FIFTEEN_MIN, max_15
        ))
        draft_scores.extend(extract_unique_scores(
            form_data, student.id, subject_id, semester_id, academic_year_id,
            '1tiet', ScoreType.ONE_PERIOD, max_1t
        ))

        final_key = f'score_final_{student.id}'
        final_val = form_data.get(final_key, type=float)
        if final_val is not None:
            draft_scores.append(DraftScore(
                student_id=student.id,
                subject_id=subject_id,
                semester_id=semester_id,
                academic_year_id=academic_year_id,
                type=ScoreType.FINAL,
                value=final_val
            ))

        db.session.add_all(draft_scores)
    db.session.commit()

def extract_unique_scores(form_data, student_id, subject_id, semester_id, academic_year_id, prefix, score_type, max_count):
    pattern = re.compile(f"score_{prefix}_{student_id}_(.+)")
    scores = []
    count = 0
    for key, val in form_data.items():
        if pattern.match(key):
            try:
                value = float(val)
                if 0 <= value <= 10:
                    scores.append(DraftScore(
                        student_id=student_id,
                        subject_id=subject_id,
                        semester_id=semester_id,
                        academic_year_id=academic_year_id,
                        type=score_type,
                        value=value
                    ))
                    count += 1
                    if count >= max_count:
                        break
            except:
                continue
    return scores

def delete_draft_scores(student_id, subject_id, semester_id, academic_year_id):
    DraftScore.query.filter_by(
        student_id=student_id,
        subject_id=subject_id,
        semester_id=semester_id,
        academic_year_id=academic_year_id
    ).delete()

def get_or_create_score_sheet(student_id, subject_id, semester_id, academic_year_id):
    sheet = get_score_sheet(student_id, subject_id, semester_id, academic_year_id)
    if not sheet:
        student = Student.query.get(student_id)

        if not student.classroom_id:
            raise ValueError(f"Student ID {student_id} không có classroom_id. Vui lòng kiểm tra dữ liệu.")

        sheet = ScoreSheet(
            student_id=student_id,
            subject_id=subject_id,
            semester_id=semester_id,
            academic_year_id=academic_year_id,
            classroom_id=student.classroom_id
        )
        db.session.add(sheet)
        db.session.flush()
    return sheet

def save_score_details(sheet, form_data, student_id):
    ScoreDetail.query.filter_by(score_sheet_id=sheet.id).delete()

    max_15, max_1t = get_score_limits(sheet.subject_id)
    for val in extract_score_values(form_data, student_id, '15', max_15):
        db.session.add(ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.FIFTEEN_MIN, value=val))
    for val in extract_score_values(form_data, student_id, '1tiet', max_1t):
        db.session.add(ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.ONE_PERIOD, value=val))

    final_key = f'score_final_{student_id}'
    final_val = form_data.get(final_key, type=float)
    if final_val is not None:
        db.session.add(ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.FINAL, value=final_val))

def extract_score_values(form_data, student_id, prefix, max_count):
    pattern = re.compile(f"score_{prefix}_{student_id}_(.+)")
    values = []
    for key, val in form_data.items():
        if pattern.match(key):
            try:
                float_val = float(val)
                if 0 <= float_val <= 10:
                    values.append(float_val)
                    if len(values) >= max_count:
                        break
            except:
                continue
    return values

def calculate_avg_score(student_id, academic_year_id, semester_id):
    scores = db.session.query(ScoreDetail.value).join(ScoreSheet).filter(
        ScoreSheet.student_id == student_id,
        ScoreSheet.academic_year_id == academic_year_id,
        ScoreSheet.semester_id == semester_id
    ).all()
    values = [s.value for s in scores]
    return sum(values) / len(values) if values else None
