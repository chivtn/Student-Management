#staff.py
from flask import render_template, request, redirect, session, jsonify
from StudentManagementApp import app, login, db
from StudentManagementApp.models import *
from StudentManagementApp.dao import staff_service as dao
from flask_login import login_user, current_user, logout_user, login_required
import string
from datetime import datetime
from flask import Blueprint

staff = Blueprint('staff', __name__, url_prefix='/staff')


@staff.route('/')
@login_required
def index():
    staff = Staff.query.filter_by(id=current_user.id).first()
    return render_template('staff/index.html', staff=staff)

@app.route("/AddStudent")
def AddStudent():
    students = dao.get_all_students()
    return render_template('staff/AddStudent.html', students=students)


@app.route("/ThemHocSinh", methods=['POST'])
def ThemHocSinh():
    err_msg = ''
    if request.method.__eq__('POST'):
        fullname = request.form.get('fullname')
        gender = request.form.get('sex')
        DoB = request.form.get('DoB')
        address = str(request.form.get('address'))
        phone = request.form.get('phonenumber')
        email = request.form.get('email')
        grade = request.form.get('grade')
        substring = email[(len(email) - 10):]
        if len(phone) != 10:
            err_msg = 'Số điện thoại sai. Vui lòng nhập lại!'
            return render_template('staff/AddStudent.html', err_msg=err_msg)
        if not substring.__eq__('@gmail.com'):
            err_msg = 'Email sai. Vui lòng nhập lại!'
            return render_template('staff/AddStudent.html', err_msg=err_msg)
        try:
            birthdate = datetime.strptime(DoB, '%Y-%m-%d')
        except:
            err_msg = 'Bạn chưa nhập ngày sinh. Vui lòng thử lại!'
            return render_template('staff/AddStudent.html', err_msg=err_msg)
        if (app.config['nambatdau'] - birthdate.year) < app.config['mintuoi'] or (
                app.config['nambatdau'] - birthdate.year) > app.config['maxtuoi']:
            err_msg = 'Ngày sinh không hợp lệ. Vui lòng thử lại!'
            return render_template('staff/AddStudent.html', err_msg=err_msg)

        student = Student(name=fullname, gender=Gender[gender], birth_date=birthdate, address=address, phone=phone,
                          email=email, grade_id=grade)
        db.session.add(student)
        db.session.commit()
        err_msg = 'Lưu thành công'
        return render_template('staff/AddStudent.html', err_msg=err_msg)


@app.route("/api/searchStudentAddStu", methods=['POST'])
def search_student_add_stu():
    name = request.json.get('searchstudentAddStu')
    grade_id = request.json.get('grade_id')

    query = Student.query.filter(Student.name.icontains(name))
    if grade_id:
        query = query.filter(Student.grade_id == grade_id)

    students = query.all()
    result = {0: {"quantity": len(students)}}
    for idx, student in enumerate(students, 1):
        result[idx] = {
            "id": student.id,
            "name": student.name,
            "sex": "Nam" if student.gender == Gender.MALE else "Nữ",
            "DoB": student.birth_date.strftime("%d/%m/%Y"),
            "address": student.address,
            "email": student.email,
            "phonenumber": student.phone,
            "grade": student.gradelevel.name.value,
            "class": student.classroom.name if student.classroom else "Chưa có lớp"
        }
    return jsonify(result)


@app.route('/api/getStudents')
def get_students_api():
    students = dao.get_all_students()
    students_data = []
    for student in students:
        students_data.append({
            "id": student.id,
            "name": student.name,
            "sex": "Nam" if student.gender == Gender.MALE else "Nữ",
            "DoB": student.birth_date.strftime("%d/%m/%Y"),
            "address": student.address,
            "email": student.email,
            "phonenumber": student.phone,
            "grade": student.gradelevel.name.value
        })
    return jsonify(students_data)


@app.route('/api/deleteStudent/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        student = dao.get_student_by_id(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Học sinh không tồn tại'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ✅ Giao diện Lập Danh Sách Lớp
@app.route("/CreateClassList")
def CreateClassList():
    result = dao.create_class_list()
    classes = result["classes"]
    unassigned_students = result["unassigned_students"]
    grades = dao.get_grade()

    return render_template('staff/CreateClassList.html',
                           classes=classes,
                           unassigned_10=unassigned_students[1],
                           unassigned_11=unassigned_students[2],
                           unassigned_12=unassigned_students[3],
                           grades=grades)


@app.route('/api/printClass', methods=['POST'])
def PrintClass():
    id_class = request.json.get('id_class')
    classroom = dao.get_classroom_by_id(id_class)
    students = dao.get_student_by_class(id_class)
    stu = {}

    stu[0] = {
        "id": classroom.id,
        "class": classroom.name,
        "quantity": len(students)
    }

    for i in range(1, len(students) + 1):
        stu[i] = {
            "name": students[i - 1].name,
            "sex": students[i - 1].gender.value,
            "DoB": students[i - 1].birth_date.strftime("%d/%m/%Y"),
            "address": students[i - 1].address
        }

    #return stu
    return jsonify(stu)


# ✅ Giao diện Chuyển Lớp cho học sinh
@app.route('/AdjustClass')
def AdjustClass():
    classes = dao.get_all_classrooms()
    grades = dao.get_grade()
    return render_template('staff/AdjustClass.html', classes=classes, grades=grades)


@app.route('/change_class', methods=['POST'])
def change_class():
    data = request.get_json()
    student_id = data.get('student_id')
    new_class_id = data.get('new_class_id')

    student = Student.query.get(student_id)
    new_class = Classroom.query.get(new_class_id)

    if not student or not new_class:
        return jsonify({"success": False, "message": "Học sinh hoặc lớp không tồn tại"}), 404

    if new_class.current_student >= app.config['soluong']:
        return jsonify({"success": False, "message": "Lớp đã đầy"}), 400

    if student.grade_id != new_class.gradelevel_id:
        return jsonify({"success": False, "message": "Không cùng khối"}), 400

    try:
        student.classroom_id = new_class.id
        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"Đã chuyển {student.name} đến lớp {new_class.name}",
            "new_class": {
                "id": new_class.id,
                "current_student": new_class.current_student
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/getClassesByGrade/<int:grade_id>')
def get_classes_by_grade(grade_id):
    classes = Classroom.query.filter_by(gradelevel_id=grade_id).all()
    return jsonify([{
        'id_class': c.id,
        'name_class': c.name
    } for c in classes])


@app.route("/api/searchStudent", methods=['POST'])
def search_student():
    data = request.get_json()
    name = data.get('searchstudent')
    class_id = data.get('class_id')

    query = Student.query.filter(Student.name.ilike(f"%{name}%"))
    if class_id:
        query = query.filter(Student.classroom_id == class_id)

    students = query.all()
    result = {0: {"quantity": len(students)}}
    for idx, student in enumerate(students, 1):
        result[idx] = {
            "id": student.id,
            "name": student.name,
            "class": student.classroom.name if student.classroom else "Chưa có lớp"
        }
    return jsonify(result)
