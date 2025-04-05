# score_service.py
from StudentManagementApp import db
from StudentManagementApp.models import ScoreSheet, ScoreDetail
from StudentManagementApp.models.enums import ScoreType

def fetch_scores_for_students(students, academic_year, semester_id, subject_id):
    scores_map = {}
    for student in students:
        sheet = get_score_sheet(student.id, subject_id, semester_id, academic_year)
        scores_map[student.id] = parse_score_sheet(sheet)
    return scores_map

def get_score_sheet(student_id, subject_id, semester_id, academic_year):
    return ScoreSheet.query.filter_by(
        student_id=student_id,
        subject_id=subject_id,
        semester_id=semester_id,
        academic_year=academic_year
    ).first()

def parse_score_sheet(sheet):
    data = {
        "score_15": [],
        "score_1tiet": [],
        "score_final": None,
        "avg": None,
        "locked": {
            "score_15": False,
            "score_1tiet": False,
            "score_final": False
        }
    }

    if not sheet:
        return data

    for detail in sheet.details:
        if detail.type == ScoreType.FIFTEEN_MIN:
            data["score_15"].append(detail.value)
        elif detail.type == ScoreType.ONE_PERIOD:
            data["score_1tiet"].append(detail.value)
        elif detail.type == ScoreType.FINAL:
            data["score_final"] = detail.value

    if len(data["score_15"]) >= 5:
        data["locked"]["score_15"] = True
    if len(data["score_1tiet"]) >= 3:
        data["locked"]["score_1tiet"] = True
    if data["score_final"] is not None:
        data["locked"]["score_final"] = True

    if is_score_complete(data):
        data["avg"] = compute_weighted_average(
            data["score_15"], data["score_1tiet"], data["score_final"]
        )

    return data

def is_score_complete(data):
    return bool(data["score_15"] and data["score_1tiet"] and data["score_final"] is not None)

def compute_weighted_average(s15, s1t, final):
    avg_15 = sum(s15) / len(s15)
    avg_1t = sum(s1t) / len(s1t)
    return round((avg_15 * 1 + avg_1t * 2 + final * 3) / 6, 2)

def store_scores(form_data, students, academic_year, semester_id, subject_id):
    for student in students:
        sheet = get_or_create_score_sheet(student.id, subject_id, semester_id, academic_year)
        save_score_details(sheet, form_data, student.id, overwrite=True)
    db.session.commit()

def save_draft_scores(form_data, students, academic_year, semester_id, subject_id):
    for student in students:
        sheet = get_or_create_score_sheet(student.id, subject_id, semester_id, academic_year)
        save_score_details(sheet, form_data, student.id, overwrite=False)
    db.session.commit()

def get_or_create_score_sheet(student_id, subject_id, semester_id, academic_year):
    sheet = get_score_sheet(student_id, subject_id, semester_id, academic_year)
    if not sheet:
        sheet = ScoreSheet(
            student_id=student_id,
            subject_id=subject_id,
            semester_id=semester_id,
            academic_year=academic_year
        )
        db.session.add(sheet)
        db.session.flush()
    return sheet

def get_score_inputs(form_data, student_id, prefix, max_count):
    values = []
    for key in form_data:
        if key.startswith(f'score_{prefix}_{student_id}_'):
            try:
                val = float(form_data[key])
                if 0 <= val <= 10:
                    values.append(val)
            except (ValueError, TypeError):
                continue
    return values[:max_count]

def save_score_details(sheet, form_data, student_id, overwrite=True):
    existing_scores = {ScoreType.FIFTEEN_MIN: [], ScoreType.ONE_PERIOD: [], ScoreType.FINAL: []}
    for d in sheet.details:
        existing_scores[d.type].append(d.value)

    new_score_15 = get_score_inputs(form_data, student_id, '15', 5)
    new_score_1tiet = get_score_inputs(form_data, student_id, '1tiet', 3)
    final_key = f'score_final_{student_id}'
    new_final_val = form_data.get(final_key, type=float)

    if overwrite:
        ScoreDetail.query.filter_by(score_sheet_id=sheet.id).delete()
        final_scores = [new_final_val] if new_final_val is not None else []
        merged_15 = new_score_15
        merged_1tiet = new_score_1tiet
    else:
        merged_15 = existing_scores[ScoreType.FIFTEEN_MIN] + new_score_15
        merged_1tiet = existing_scores[ScoreType.ONE_PERIOD] + new_score_1tiet
        final_scores = existing_scores[ScoreType.FINAL]
        if new_final_val is not None and not final_scores:
            final_scores = [new_final_val]
        # Xóa cũ trước khi ghi lại bản mới
        ScoreDetail.query.filter_by(score_sheet_id=sheet.id).delete()

    for val in merged_15[:5]:
        db.session.add(ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.FIFTEEN_MIN, value=val))
    for val in merged_1tiet[:3]:
        db.session.add(ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.ONE_PERIOD, value=val))
    if final_scores:
        db.session.add(ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.FINAL, value=final_scores[0]))

def is_valid_score(value):
    try:
        return 0 <= float(value) <= 10
    except (TypeError, ValueError):
        return False

def calculate_avg_score(student_id, academic_year, semester_id):
    scores = db.session.query(ScoreDetail.value).join(ScoreSheet).filter(
        ScoreSheet.student_id == student_id,
        ScoreSheet.academic_year == academic_year,
        ScoreSheet.semester_id == semester_id
    ).all()
    values = [s.value for s in scores]
    return sum(values) / len(values) if values else None

def save_quick_input_scores(students, form_data, subject_id, semester_id, academic_year):
    errors = []
    for student in students:
        score_15 = form_data.get(f'score_15_{student.id}', type=float)
        score_1tiet = form_data.get(f'score_1tiet_{student.id}', type=float)
        score_final = form_data.get(f'score_final_{student.id}', type=float)

        if None in (score_15, score_1tiet, score_final):
            errors.append(f"⚠️ Học sinh {student.full_name} thiếu điểm.")
            continue

        if not all(map(is_valid_score, [score_15, score_1tiet, score_final])):
            errors.append(f"❌ Điểm không hợp lệ cho {student.full_name}. Chỉ cho phép từ 0 đến 10.")
            continue

        sheet = get_or_create_score_sheet(student.id, subject_id, semester_id, academic_year)
        ScoreDetail.query.filter_by(score_sheet_id=sheet.id).delete()

        db.session.add(ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.FIFTEEN_MIN, value=score_15))
        db.session.add(ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.ONE_PERIOD, value=score_1tiet))
        db.session.add(ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.FINAL, value=score_final))

    return errors
