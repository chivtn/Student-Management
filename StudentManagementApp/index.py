from flask import render_template, request, redirect, session, jsonify
from StudentManagementApp import app, login, db, utils
from StudentManagementApp.models import *
import dao
from flask_login import login_user, current_user, logout_user
from StudentManagementApp import admin
import string
from datetime import datetime
from StudentManagementApp.utils import update_regulation


# ✅ Giao diện Đăng Nhập
@app.route("/")
def index():
    return render_template('layout/base.html')

@app.route('/admin/login', methods=['post'])
def login_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    admin = dao.auth_admin(username=username, password=password)
    if admin:
        login_user(admin)

    return redirect('/admin')

@app.route('/login', methods=['get', 'post'])
def login_view():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        staff = dao.auth_staff(username=username, password=password)
        if staff:
            login_user(staff)
            return render_template('staff.html')
        else:
            err_msg = 'Tên đăng nhập hoặc mật khẩu không chính xác. Vui lòng thử lại!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/logout')
def logout_view():
    logout_user()
    return redirect('/login')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def inject_regulations():
    max_per_class = dao.get_regulation_value("Quy định số lượng học sinh trong 1 lớp")
    return dict(max_per_class=max_per_class)

# ✅ Phần Chi
# ✅ Giao diện Thêm Học Sinh
@app.route("/AddStudent")
def AddStudent():
    students = dao.get_student()
    return render_template('AddStudent.html', students=students)


@app.route("/ThemHocSinh", methods=['POST'])
def ThemHocSinh():
    err_msg = ''
    if request.method.__eq__('POST'):
        fullname = request.form.get('fullname')
        sex = request.form.get('sex')
        DoB = request.form.get('DoB')
        address = str(request.form.get('address'))
        phonenumber = request.form.get('phonenumber')
        email = request.form.get('email')
        grade = request.form.get('grade')
        substring = email[(len(email) - 10):]
        if len(phonenumber) != 10:
            err_msg = 'Số điện thoại sai. Vui lòng nhập lại!'
            return render_template('AddStudent.html', err_msg=err_msg)
        if not substring.__eq__('@gmail.com'):
            err_msg = 'Email sai. Vui lòng nhập lại!'
            return render_template('AddStudent.html', err_msg=err_msg)
        try:
            birthdate = datetime.strptime(DoB, '%Y-%m-%d')
        except:
            err_msg = 'Bạn chưa nhập ngày sinh. Vui lòng thử lại!'
            return render_template('AddStudent.html', err_msg=err_msg)

        min_age = dao.get_regulation_value("Quy định số tuổi nhỏ nhất của học sinh")
        max_age = dao.get_regulation_value("Quy định số tuổi lớn nhất của học sinh")
        current_year = datetime.now().year  # Giả sử nambatdau là năm hiện tại
        if (current_year - birthdate.year) < min_age or (current_year - birthdate.year) > max_age:
            err_msg = 'Ngày sinh không hợp lệ. Vui lòng thử lại!'
            return render_template('AddStudent.html', err_msg=err_msg)

        student = Student(name=fullname, sex=sex, DoB=DoB, address=address, phonenumber=phonenumber,
                          email=email, id_grade=grade)
        db.session.add(student)
        db.session.commit()
        err_msg = 'Lưu thành công'
        return render_template('AddStudent.html', err_msg=err_msg)


@app.route("/api/searchStudentAddStu", methods=['POST'])
def search_student_add_stu():
    name = request.json.get('searchstudentAddStu')
    grade_id = request.json.get('grade_id')  # Lấy giá trị khối từ request

    # Tạo query lọc theo tên và khối (nếu có)
    query = Student.query.filter(Student.name.icontains(name))
    if grade_id:
        query = query.filter(Student.id_grade == grade_id)

    students = query.all()
    result = {0: {"quantity": len(students)}}
    for idx, student in enumerate(students, 1):
        result[idx] = {
            "id": student.id,
            "name": student.name,
            "sex": "Nam" if student.sex.name == 'MALE' else "Nữ",
            "DoB": student.DoB.strftime("%d/%m/%Y"),
            "address": student.address,
            "email": student.email,
            "phonenumber": student.phonenumber,
            "grade": student.Grade.name_grade.value,
            "class": student.Class.name_class if student.Class else "Chưa có lớp"
        }
    return jsonify(result)


@app.route('/api/getStudents')
def get_students_api():
    students = dao.get_student()
    students_data = []
    for student in students:
        students_data.append({
            "id": student.id,
            "name": student.name,
            "sex": "Nam" if student.sex.name == 'MALE' else "Nữ",
            "DoB": student.DoB.strftime("%d/%m/%Y"),
            "address": student.address,
            "email": student.email,
            "phonenumber": student.phonenumber,
            "grade": student.Grade.name_grade.value
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

    return render_template('CreateClassList.html',
                           classes=classes,
                           unassigned_10=unassigned_students[1],
                           unassigned_11=unassigned_students[2],
                           unassigned_12=unassigned_students[3],
                           grades=grades)


@app.route('/api/printClass', methods=['post'])
def PrintClass():
    id_class = request.json.get('id_class')
    classes = dao.get_class_by_id(id_class)
    students = dao.get_student_by_class(id_class)
    stu = {}

    stu[0] = {
        "id": classes.id_class,
        "class": classes.name_class,
        "quantity": len(students)
    }

    for i in range(1, len(students) + 1):
        stu[i] = {
            "name": students[i - 1].name,
            "sex": students[i - 1].sex.value,
            "DoB": students[i - 1].DoB.strftime("%d/%m/%Y"),
            "address": students[i - 1].address
        }

    return stu

# ✅ Giao diện Chuyển Lớp cho học sinh
# Route để hiển thị trang chuyển lớp
@app.route('/AdjustClass', methods=['GET'])
def AdjustClass():
    classes = Class.query.all()
    grades = dao.get_grade()
    return render_template('AdjustClass.html', classes=classes, grades=grades)


@app.route('/change_class', methods=['POST'])
def change_class():
    data = request.get_json()
    student_id = data.get('student_id')
    new_class_id = data.get('new_class_id')

    student = Student.query.get(student_id)
    new_class = Class.query.get(new_class_id)

    if not student or not new_class:
        return jsonify({"success": False, "message": "Học sinh hoặc lớp không tồn tại"}), 404

    # Lấy giá trị quy định mới nhất từ database
    max_per_class = dao.get_regulation_value("Quy định số lượng học sinh trong 1 lớp")

    # Kiểm tra lớp mới có đầy không
    if new_class.current_student >= max_per_class:
        return jsonify({"success": False, "message": "Lớp đã đầy"}), 400

    # Kiểm tra cùng khối
    if student.id_grade != new_class.id_grade:
        return jsonify({"success": False, "message": "Không cùng khối"}), 400

    old_class_id = student.id_class
    try:
        # Cập nhật lớp mới
        student.id_class = new_class.id_class
        db.session.commit()

        # Refresh thông tin lớp cũ và mới
        db.session.refresh(new_class)
        if old_class_id:
            old_class = Class.query.get(old_class_id)
            db.session.refresh(old_class)
        else:
            old_class = None

        # ✅ Lấy giá trị quy định mới nhất
        max_per_class = dao.get_regulation_value("Quy định số lượng học sinh trong 1 lớp")

        return jsonify({
            "success": True,
            "message": f"Đã chuyển {student.name} đến lớp {new_class.name_class}",
            "old_class": {
                "id": old_class.id_class if old_class else None,
                "name": old_class.name_class if old_class else None,
                "current_student": old_class.current_student if old_class else 0
            },
            "new_class": {
                "id": new_class.id_class,
                "name": new_class.name_class,
                "current_student": new_class.current_student
            },
            "max_per_class": max_per_class  # ✅ Thêm giá trị quy định vào response
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/getClassesByGrade/<int:grade_id>')
def get_classes_by_grade(grade_id):
    classes = Class.query.filter_by(id_grade=grade_id).all()
    return jsonify([{
        'id_class': c.id_class,
        'name_class': c.name_class
    } for c in classes])


# Route tìm kiếm học sinh
@app.route("/api/searchStudent", methods=['POST'])
def search_student():
    data = request.get_json()
    name = data.get('searchstudent')
    class_id = data.get('class_id')

    query = Student.query.filter(Student.name.icontains(name))
    # students = dao.get_student_by_name(name)

    if class_id:
        query = query.filter(Student.id_class == class_id)

    students = query.all()
    result = {0: {"quantity": len(students)}}
    for idx, student in enumerate(students, 1):
        result[idx] = {
            "id": student.id,
            "name": student.name,
            "class": student.Class.name_class if student.Class else "Chưa có lớp"
        }
    return jsonify(result)

# ✅ Phần Giang
@app.route("/api/statisticsScore", methods=['POST'])
def StatisticsScore():
    id_subject = request.json.get('id_subject')
    id_semester = request.json.get('id_semester')
    classes = dao.get_class()
    semester = 0
    schoolyear = ''
    if int(id_semester) % 2 == 0:
        semester = 2
    else:
        semester = 1
    if id_semester == '1':
        schoolyear = 'Năm học 2020-2021'
    elif id_semester == '3':
        schoolyear = 'Năm học 2021-2022'
    elif id_semester == '5':
        schoolyear = 'Năm học 2022-2023'
    elif id_semester == '7':
        schoolyear = 'Năm học 2023-2024'
    stu = {}
    stu[0] = {
        'subject': dao.get_subject_by_id(id_subject).name_subject,
        'semester': semester,
        'schoolyear': schoolyear,
        'quantity': len(classes)
    }
    for i in range(len(classes)):
        statistics = dao.statistics_subject(id_class=classes[i].id_class, id_subject=id_subject, id_semester=id_semester)
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
            'class': classes[i].name_class,
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

    classes = dao.get_class()
    max_student = max(len(dao.get_student_by_class(c.id_class)) for c in classes)

    if quantity < max_student:
        return jsonify({
            'status': 200,
            'content': f'Sĩ số tối đa phải lớn hơn {max_student}. Vui lòng kiểm tra lại!'
        })

    # ✅ Cập nhật xuống DB
    update_regulation("Quy định số lượng học sinh trong 1 lớp", quantity)
    update_regulation("Quy định số tuổi nhỏ nhất của học sinh", min_age)
    update_regulation("Quy định số tuổi lớn nhất của học sinh", max_age)

    return jsonify({'status': 500, 'content': 'Thành công!'})

if __name__ == '__main__':
    app.run(debug=True)
