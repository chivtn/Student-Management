from flask import render_template, request, redirect, session, jsonify
from StudentManagementApp import app, login, db, utils
from StudentManagementApp.models import *
import dao
from flask_login import login_user, current_user, logout_user
from StudentManagementApp import admin
import string
from datetime import datetime


# ✅ Giao diện Đăng Nhập
@app.route("/")
def index():
    return render_template('layout/base.html')


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
        if (app.config['nambatdau'] - birthdate.year) < app.config['mintuoi'] or (
                app.config['nambatdau'] - birthdate.year) > app.config['maxtuoi']:
            err_msg = 'Ngày sinh không hợp lệ. Vui lòng thử lại!'
            return render_template('AddStudent.html', err_msg=err_msg)

        student = Student(name=fullname, sex=sex, DoB=DoB, address=address, phonenumber=phonenumber,
                          email=email, id_grade=grade)
        db.session.add(student)
        db.session.commit()
        # Gọi hàm tự động phân lớp sau khi thêm học sinh
        dao.create_class_list()
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


@app.route('/api/addClass', methods=['POST'])
def add_new_class():
    data = request.get_json()
    grade_id = data.get('grade_id')

    # Lấy tên khối từ grade_id (ví dụ: 1 -> "10")
    grade_name = {
        1: "10",
        2: "11",
        3: "12"
    }.get(grade_id, "10")

    # Tìm lớp có số thứ tự cao nhất trong khối
    # Trong route /api/addClass (index.py)
    last_class = Class.query.filter(Class.id_grade == grade_id) \
        .order_by(Class.id_class.desc()).first()  # Sửa thành sắp xếp theo id_class

    if last_class:
        # Tách số từ tên lớp (ví dụ: "10A10" -> 10, "A5" -> 5)
        import re
        match = re.search(r'A(\d+)$', last_class.name_class)
        if match:
            last_number = int(match.group(1))
            new_number = last_number + 1
        else:
            # Xử lý trường hợp tên lớp không đúng định dạng
            new_number = 1
    else:
        new_number = 1

    # Tạo tên lớp mới (đảm bảo định dạng "Khối + A + số")
    grade_name = {1: "10", 2: "11", 3: "12"}.get(grade_id, "10")
    new_class_name = f"{grade_name}A{new_number}"

    try:
        new_class = Class(name_class=new_class_name, id_grade=grade_id)
        db.session.add(new_class)
        db.session.commit()
        return jsonify({"success": True, "message": "Thêm lớp thành công"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/deleteClass/<int:class_id>', methods=['DELETE'])
def delete_class(class_id):
    try:
        class_to_delete = Class.query.get(class_id)
        if not class_to_delete:
            return jsonify({"success": False, "error": "Lớp không tồn tại"}), 404

        # Cập nhật học sinh trong lớp về chưa phân lớp
        students = Student.query.filter(Student.id_class == class_id).all()
        for student in students:
            student.id_class = None
            db.session.commit()

        # Xóa lớp
        db.session.delete(class_to_delete)
        db.session.commit()

        return jsonify({"success": True, "message": "Xóa lớp thành công"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


# ✅ Giao diện Chuyển Lớp cho học sinh

# Route để hiển thị trang chuyển lớp
@app.route('/AdjustClass', methods=['GET'])
def AdjustClass():
    classes = Class.query.all()
    grades = dao.get_grade()
    return render_template('AdjustClass.html', classes=classes, grades=grades)


# Route chuyển lớp
@app.route('/change_class', methods=['POST'])
def change_class():
    data = request.get_json()
    student_id = data.get('student_id')
    new_class_id = data.get('new_class_id')

    student = Student.query.get(student_id)
    new_class = Class.query.get(new_class_id)

    if not student or not new_class:
        return jsonify({"success": False, "message": "Học sinh hoặc lớp không tồn tại"}), 404

    # Lấy lớp cũ của học sinh
    old_class_id = student.id_class
    old_class = Class.query.get(old_class_id) if old_class_id else None

    # Kiểm tra lớp mới có đầy không (giả sử mỗi lớp tối đa 40 học sinh)
    if new_class.current_student >= 40:  # Nơi cần sửa
        return jsonify({"success": False, "message": "Lớp đã đầy"}), 400

    # Kiểm tra học sinh có cùng khối với lớp mới không
    if student.id_grade != new_class.id_grade:
        return jsonify({"success": False, "message": "Không cùng khối"}), 400

    try:
        student.id_class = new_class.id_class
        db.session.commit()

        # Lấy lại thông tin lớp cũ và mới sau khi commit
        updated_old_class = Class.query.get(old_class_id) if old_class_id else None
        updated_new_class = Class.query.get(new_class_id)

        return jsonify({
            "success": True,
            "message": f"Đã chuyển {student.name} đến lớp {new_class.name_class}",
            "old_class": {
                "id": updated_old_class.id_class if updated_old_class else None,
                "current_student": updated_old_class.current_student if updated_old_class else 0
            },
            "new_class": {
                "id": new_class.id_class,
                "current_student": new_class.current_student + 1
            }
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

if __name__ == '__main__':
    app.run(debug=True)
