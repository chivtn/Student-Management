#routes/admin.py
from flask import render_template, request, jsonify
from StudentManagementApp import app, db, utils
from StudentManagementApp.models import Regulation
from StudentManagementApp.dao import staff_service, stat_service

# === API: Thống kê điểm theo môn học ===
@app.route("/api/statisticsScore", methods=['POST'])
def StatisticsScore():
    id_subject = request.json.get('id_subject')
    id_semester = request.json.get('id_semester')

    classes = staff_service.get_all_classrooms()
    semester, schoolyear = utils.get_school_year_and_semester(id_semester)

    result = {
        0: {
            'subject': staff_service.get_subject_by_id(id_subject).name,
            'semester': semester,
            'schoolyear': schoolyear,
            'quantity': len(classes)
        }
    }

    for idx, classroom in enumerate(classes, start=1):
        statistics = stat_service.statistics_subject(
            classroom_id=classroom.id,
            subject_id=id_subject,
            semester_id=id_semester
        )
        passed_count = sum(1 for s in statistics if s['score'] >= 5)
        total = len(statistics)
        rate = round((passed_count / total) * 100, 1) if total else 0

        result[idx] = {
            'class': classroom.name,
            'quantity_student': total,
            'quantity_passed': passed_count,
            'rate': rate
        }

    return result

# === API: Thay đổi quy định sĩ số và độ tuổi ===
@app.route("/api/changeRule", methods=['POST'])
def ChangeRule():
    quantity = int(request.json.get('quantity'))
    min_age = int(request.json.get('min_age'))
    max_age = int(request.json.get('max_age'))

    # Kiểm tra hợp lệ
    if quantity <= 0 or min_age <= 0 or max_age <= 0:
        return jsonify({'status': 500, 'content': 'Thông tin không hợp lệ. Vui lòng kiểm tra lại!'})
    if min_age >= max_age:
        return jsonify({'status': 500, 'content': 'Tuổi lớn nhất phải lớn hơn tuổi nhỏ nhất. Vui lòng kiểm tra lại!'})

    # Lấy sĩ số lớp lớn nhất để kiểm tra
    classes = staff_service.get_all_classrooms()
    max_students = max((len(staff_service.get_student_by_class(c.id)) for c in classes), default=0)
    if quantity < max_students:
        return jsonify({
            'status': 500,
            'content': f'Sĩ số tối đa phải lớn hơn hoặc bằng {max_students}. Vui lòng kiểm tra lại!'
        })

    # Cập nhật hoặc tạo mới bản ghi Regulation
    rule = Regulation.query.first()
    if not rule:
        rule = Regulation(min_age=min_age, max_age=max_age, max_class_size=quantity)
        db.session.add(rule)
    else:
        rule.min_age = min_age
        rule.max_age = max_age
        rule.max_class_size = quantity

    db.session.commit()

    return jsonify({'status': 200, 'content': 'Thay đổi quy định thành công!'})
