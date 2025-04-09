from multiprocessing import connection
import random
from StudentManagementApp.models import *
from StudentManagementApp import app
import hashlib
from sqlalchemy import func
from flask import jsonify


# Phần Chi
def get_user_by_id(user_id):
    return User.query.get(user_id)

#
def auth_staff(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password), User.user_role.__eq__(UserRoleEnum.STAFF)).first()

# Yêu Cầu 2
def get_class():
    return Class.query.all()

def get_class_by_id_grade(id_grade):
    return Class.query.filter(Class.id_grade.__eq__(id_grade)).all()

def get_class_by_id(id_class):
    return Class.query.filter(Class.id_class.__eq__(id_class)).first()

# Phần quy định mới
def get_regulation_value(regulation_name):
    regulation = Regulation.query.filter_by(name_regulations=regulation_name).first()
    return regulation.value_regulations if regulation else None

def get_class_is_blank(id_grade):
    # Lấy tất cả lớp thuộc khối
    classes = Class.query.filter(Class.id_grade == id_grade).all()
    # Lọc lớp chưa đầy
    return [c for c in classes if c.current_student < get_regulation_value("Quy định số lượng học sinh trong 1 lớp")]

# Hàm này Giang dùm kh, này quan trọng bên t
# def get_class_is_blank():
#     classes = Class.query.all()
#     classes_blank = []
#     for c in classes:
#         if len(c.students) < app.config['soluong']:
#             classes_blank.append(c)
#     return classes_blank

def get_student_by_class(id_class):
    return Student.query.filter(Student.id_class.__eq__(id_class)).all()

def get_student():
    return Student.query.all()

def get_student_by_name(name, class_id=None):
    query = Student.query.filter(Student.name.icontains(name))
    if class_id:
        query = query.filter(Student.id_class == class_id)
    return query.all()


def get_student_by_id(id):
    return Student.query.get(id)


def get_student_by_id_grade(id_grade):
    return Student.query.filter(Student.id_grade == id_grade).all()


def get_subject():
    return Subject.query.all()


def get_subject_by_id(id):
    return Subject.query.filter(Subject.id_subject == id).first()


def get_semester():
    return Semester.query.all()


def get_semester_by_id(id):
    return Semester.query.filter(Semester.id_semester == id).first()


def get_grade():
    return Grade.query.all()


def create_class_list():
    grades = get_grade()
    unassigned_students = {1: [], 2: [], 3: []}

    for g in grades:
        students = get_student_by_id_grade(g.id_grade)
        unassigned = [s for s in students if not s.id_class]
        max_per_class = get_regulation_value("Quy định số lượng học sinh trong 1 lớp")

        # Bước 1: Tính số lớp cần thiết
        required_classes = len(unassigned) // max_per_class
        if len(unassigned) % max_per_class != 0:
            required_classes += 1

        # Bước 2: Tạo thêm lớp nếu thiếu
        current_classes = Class.query.filter(Class.id_grade == g.id_grade).all()
        current_class_count = len(current_classes)

        # Tạo lớp mới nếu cần
        if current_class_count < required_classes:
            for _ in range(required_classes - current_class_count):
                last_class = Class.query.filter(Class.id_grade == g.id_grade) \
                    .order_by(Class.id_class.desc()).first()
                grade_name = {1: "10", 2: "11", 3: "12"}.get(g.id_grade, "10")
                new_number = int(last_class.name_class.split("A")[1]) + 1 if last_class else 1
                new_class_name = f"{grade_name}A{new_number}"
                new_class = Class(name_class=new_class_name, id_grade=g.id_grade)
                db.session.add(new_class)
                db.session.commit()
                current_classes.append(new_class)

        # Bước 3: Phân bổ học sinh đều vào các lớp
        available_classes = current_classes.copy()
        random.shuffle(unassigned)  # Xáo trộn học sinh

        for idx, student in enumerate(unassigned):
            target_class = available_classes[idx % len(available_classes)]
            if target_class.current_student < max_per_class:
                student.id_class = target_class.id_class
                db.session.commit()
            else:
                # Tìm lớp chưa đầy đầu tiên
                for cls in available_classes:
                    if cls.current_student < max_per_class:
                        student.id_class = cls.id_class
                        db.session.commit()
                        break

        # Bước 4: Cập nhật lại danh sách chưa phân lớp
        current_classes = Class.query.filter(Class.id_grade == g.id_grade).all()
        for student in get_student_by_id_grade(g.id_grade):
            if not student.id_class:
                unassigned_students[g.id_grade].append(student)

    return {
        "classes": get_class(),
        "unassigned_students": unassigned_students
    }




# Phần Giang
def statistics_subject(id_class, id_subject, id_semester):
    student = get_student_by_class(id_class)
    scores = {}

    for i in range(len(student)):
        scores[i] = {
            'id_student': student[i].id,
            'score': 0,
        }
    test_15m = db.session.query(Test.id_student, func.sum(Test.score), func.count(Test.score)) \
        .join(Student, Student.id == Test.id_student) \
        .filter(Test.id_semester == id_semester, Test.id_subject == id_subject,
                Student.id_class == id_class, Test.type == '15 phút') \
        .group_by(Test.id_student).all()

    test_45m = db.session.query(Test.id_student, func.sum(Test.score), func.count(Test.score)) \
        .join(Student, Student.id == Test.id_student) \
        .filter(Test.id_semester == id_semester, Test.id_subject == id_subject,
                Student.id_class == id_class, Test.type == '1 tiết') \
        .group_by(Test.id_student).all()

    test_final = db.session.query(Test.id_student, func.sum(Test.score), func.count(Test.score)) \
        .join(Student, Student.id == Test.id_student) \
        .filter(Test.id_semester == id_semester, Test.id_subject == id_subject,
                Student.id_class == id_class, Test.type == 'Cuối kỳ') \
        .group_by(Test.id_student).all()
    if test_15m and test_45m and test_final:
        for i in range(len(test_15m)):
            a = float(test_15m[i][1])
            b = float(test_45m[i][1])
            c = float(test_final[i][1])
            x = int(test_15m[i][2])
            y = int(test_45m[i][2])
            z = int(test_final[i][2])
            scores[i]['score'] = round((a + b * 2 + c * 3) / (x + y * 2 + z * 3), 1)
    return scores

def count_users():
    return User.query.count()

# Thêm hàm đếm số lượng môn học
def count_subjects():
    return Subject.query.count()

def auth_admin(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password), User.user_role.__eq__(UserRoleEnum.ADMIN)).first()


if __name__ == '__main__':
    with app.app_context():
        print(create_class_list())
