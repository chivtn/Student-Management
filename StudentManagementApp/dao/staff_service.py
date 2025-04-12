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

def get_regulation_value(attr):
    rule = Regulation.query.first()
    if not rule:
        return None
    if attr == "min_age":
        return rule.min_age
    elif attr == "max_age":
        return rule.max_age
    elif attr == "max_class_size":
        return rule.max_class_size
    return None

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

def get_student_by_class(classroom_id):
   # return Student.query.filter(Student.classroom_id == classroom_id).all()
    #return Student.query.filter(Student.classroom_id.__eq__(classroom_id)).all()
   return Student.query.filter_by(classroom_id=classroom_id).all()


def get_students_by_gradelevel(grade_id):
   # return Student.query.filter_by(grade_id=grade_id).all()
    #return Student.query.filter(Student.grade_id.__eq__(grade_id)).all()
   return Student.query.filter_by(grade_id=grade_id).all()

def search_students_by_name(name, classroom_id=None):
    query = Student.query.filter(Student.name.ilike(f"%{name}%"))
    if classroom_id:
        query = query.filter_by(classroom_id=classroom_id)
    return query.all()

# --- SUBJECTS ---
def get_subject():
    return Subject.query.all()

def get_subject_by_id(subject_id):
    #return Subject.query.filter(Subject.id == subject_id).first()
    return Subject.query.get(subject_id)

# --- SEMESTERS ---
def get_semester():
    return Semester.query.all()

def get_semester_by_id(semester_id):
    #return Semester.query.filter(Semester.id == semester_id).first()
    return Semester.query.get(semester_id)

# --- GRADELEVELS ---
def get_grade():
    return GradeLevel.query.all()

# --- CLASS ASSIGNMENT ---
def create_class_list():
    grades = get_grade()
    unassigned_students = {g.id: [] for g in grades}
  #  max_per_class = app.config['soluong']

    for g in grades:
        students = get_students_by_gradelevel(g.id)
        unassigned = [s for s in students if not s.classroom_id]
        max_per_class = get_regulation_value("max_class_size")

        current_classes = get_classrooms_by_gradelevel(g.id)
        if not current_classes:
            new_class = Classroom(name=f"{g.name.value}A1", gradelevel_id=g.id, academic_year=str(datetime.now().year))
            db.session.add(new_class)
            db.session.commit()
            current_classes = [new_class]

        required_classes = max((len(unassigned) + max_per_class - 1) // max_per_class, len(current_classes))

        while len(current_classes) < required_classes:
            last_class = Classroom.query.filter_by(gradelevel_id=g.id).order_by(Classroom.name.desc()).first()
            suffix = int(last_class.name.split("A")[-1]) + 1 if last_class else 1
            new_class = Classroom(name=f"{g.name.value}A{suffix}", gradelevel_id=g.id,
                                  academic_year=str(datetime.now().year))
            db.session.add(new_class)
            db.session.commit()
            current_classes.append(new_class)

        sorted_classes = sorted(current_classes, key=lambda c: c.current_student)

        for student in unassigned:
            for cls in sorted_classes:
                if cls.current_student < max_per_class:
                    student.classroom_id = cls.id
                    db.session.commit()
                    break

        unassigned_students[g.id] = [s for s in students if not s.classroom_id]

    return {
        "classes": get_all_classrooms(),
        "unassigned_students": unassigned_students
    }
