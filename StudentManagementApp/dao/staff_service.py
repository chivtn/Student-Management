#staff.service
import random
import hashlib
from StudentManagementApp.models import *
from StudentManagementApp import app, db
from sqlalchemy import func

# --- AUTH ---
def get_user_by_id(user_id):
    return User.query.get(user_id)

def auth_staff(username, password):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    return User.query.filter_by(username=username, password=password, role=Role.STAFF).first()

# --- CLASSROOMS ---
def get_all_classrooms():
    return Classroom.query.all()

def get_classroom_by_id(classroom_id):
    return Classroom.query.get(classroom_id)

def get_classrooms_by_gradelevel(gradelevel_id):
    return Classroom.query.filter_by(gradelevel_id=gradelevel_id).all()

def get_blank_classrooms():
    return [c for c in Classroom.query.all() if len(c.students) < app.config['soluong']]

# --- STUDENTS ---
def get_all_students():
    return Student.query.all()

def get_student_by_id(student_id):
    return Student.query.get(student_id)

def get_student_by_class(id_class):
   # return Student.query.filter(Student.classroom_id == id_class).all()
    return Student.query.filter(Student.classroom_id.__eq__(id_class)).all()


def get_students_by_gradelevel(id_grade):
   # return Student.query.filter_by(grade_id=id_grade).all()
    return Student.query.filter(Student.grade_id.__eq__(id_grade)).all()


def search_students_by_name(name, classroom_id=None):
    query = Student.query.filter(Student.name.ilike(f"%{name}%"))
    if classroom_id:
        query = query.filter_by(classroom_id=classroom_id)
    return query.all()

# --- SUBJECTS ---
def get_subject():
    return Subject.query.all()

def get_subject_by_id(subject_id):
    return Subject.query.filter(Subject.id == subject_id).first()

# --- SEMESTERS ---
def get_semester():
    return Semester.query.all()

def get_semester_by_id(semester_id):
    return Semester.query.filter(Semester.id == semester_id).first()

# --- GRADELEVELS ---
def get_grade():
    return GradeLevel.query.all()

# --- CLASS ASSIGNMENT ---
def create_class_list():
    grades = get_grade()
    unassigned_students = {g.id: [] for g in grades}
    max_per_class = app.config['soluong']

    for g in grades:
        students = get_students_by_gradelevel(g.id)
        unassigned = [s for s in students if not s.classroom_id]

        # Số lớp cần thiết
        required_classes = (len(unassigned) + max_per_class - 1) // max_per_class

        current_classes = Classroom.query.filter_by(gradelevel_id=g.id).all()

        # Tạo lớp mới nếu cần
        if len(current_classes) < required_classes:
            for _ in range(required_classes - len(current_classes)):
                last_class = Classroom.query.filter_by(gradelevel_id=g.id).order_by(Classroom.id.desc()).first()
                last_number = int(last_class.name.split('A')[1]) if last_class else 0
                new_name = f"{g.name.value}A{last_number + 1}"
                new_class = Classroom(name=new_name, gradelevel_id=g.id, academic_year="2024-2025")
                db.session.add(new_class)
                db.session.commit()
                current_classes.append(new_class)

        # Phân bổ học sinh
        random.shuffle(unassigned)
        for idx, student in enumerate(unassigned):
            for cls in current_classes:
                if len(cls.students) < max_per_class:
                    student.classroom_id = cls.id
                    db.session.commit()
                    break

        # Cập nhật danh sách chưa phân lớp
        for student in get_students_by_gradelevel(g.id):
            if not student.classroom_id:
                unassigned_students[g.id].append(student)

    return {
        "classes": get_all_classrooms(),
        "unassigned_students": unassigned_students
    }
