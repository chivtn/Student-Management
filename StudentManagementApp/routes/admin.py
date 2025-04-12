#admin.py
from flask import render_template, request, redirect, session, jsonify
from StudentManagementApp import app, login, db, utils
from StudentManagementApp.models import *
from StudentManagementApp.dao import staff_service, stat_service
from flask_login import login_user, current_user, logout_user
from StudentManagementApp import admin_view
import string
from datetime import datetime

# ✅ Phần Giang
@app.route("/api/statisticsScore", methods=['POST'])
def StatisticsScore():
    id_subject = request.json.get('id_subject')
    id_semester = request.json.get('id_semester')
    classes = staff_service.get_all_classrooms()
    semester = 0
    schoolyear = ''
    if int(id_semester) % 2 == 0:
        semester = 2
    else:
        semester = 1
    if id_semester == '1':
        schoolyear = '2020-2021'
    elif id_semester == '3':
        schoolyear = '2021-2022'
    elif id_semester == '5':
        schoolyear = '2022-2023'
    elif id_semester == '7':
        schoolyear = '2023-2024'
    stu = {}
    stu[0] = {
        'subject': staff_service.get_subject_by_id(id_subject).name,
        'semester': semester,
        'schoolyear': schoolyear,
        'quantity': len(classes)
    }
    for i in range(len(classes)):
        statistics = stat_service.statistics_subject(
            classroom_id=classes[i].id,
            subject_id=id_subject,
            semester_id=id_semester
        )
        count = 0
        for j in range(len(statistics)):
            if statistics[j]['score'] >= 5:
                count = count + 1
        rate = 0
        if len(statistics) == 0:
            rate = 0
        else:
            rate = round(float(count / len(statistics) * 100), 1)
        stu[i+1]= {
            'class': classes[i].name,
            'quantity_student': len(statistics),
            'quantity_passed': count,
            'rate': rate
        }
    return stu

@app.route("/api/changeRule", methods=['POST'])
def ChangeRule():
    quantity = int(request.json.get('quantity'))
    min_age = int(request.json.get('min_age'))
    max_age = int(request.json.get('max_age'))

    if quantity <= 0 or min_age <= 0 or max_age <= 0:
        return jsonify({'status': 200, 'content': 'Thông tin không hợp lệ. Vui lòng kiểm tra lại!'})
    if min_age >= max_age:
        return jsonify({'status': 200, 'content': 'Tuổi lớn nhất phải lớn hơn tuổi nhỏ nhất. Vui lòng kiểm tra lại!'})
    classes = staff_service.get_all_classrooms()
    max = 0
    for c in classes:
        student = staff_service.get_student_by_class(c.id)
        if max < len(student):
            max = len(student)
    if quantity < max:
        return jsonify({'status': 200, 'content': str.format('Sĩ số tối đa phải lớn hơn {0}. Vui lòng kiểm tra lại!', max)})
    app.config['soluong'] = quantity
    app.config['mintuoi'] = min_age
    app.config['maxtuoi'] = max_age
    return jsonify({'status': 500, 'content': 'Thành công!'})
