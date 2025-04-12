from StudentManagementApp import app, db
from StudentManagementApp.models import *
from faker import Faker
from werkzeug.security import generate_password_hash
from datetime import date
import random

fake = Faker('vi_VN')

with app.app_context():
    db.drop_all()
    db.create_all()

    # --- Quy định ---
    db.session.add(Regulation(min_age=15, max_age=20, max_class_size=45))

    # --- Khối lớp ---
    grade10 = GradeLevel(id=1, name=Grade.GRADE_10)
    grade11 = GradeLevel(id=2, name=Grade.GRADE_11)
    grade12 = GradeLevel(id=3, name=Grade.GRADE_12)
    db.session.add_all([grade10, grade11, grade12])
    db.session.flush()

    # --- Môn học ---
    subjects = [
        Subject(name="Toán", gradelevel=grade10),
        Subject(name="Văn", gradelevel=grade10),
        Subject(name="Anh", gradelevel=grade10),
        Subject(name="Lý", gradelevel=grade11),
        Subject(name="Hóa", gradelevel=grade11),
        Subject(name="Sinh", gradelevel=grade11),
        Subject(name="Tin", gradelevel=grade12),
        Subject(name="GDCD", gradelevel=grade12)
    ]
    db.session.add_all(subjects)
    db.session.flush()

    # --- Người dùng ---
    admin = User(id=1, username='admin', password=generate_password_hash('admin123'), role=Role.ADMIN)
    teacher = User(id=2, username='teacher1', password=generate_password_hash('teacher123'), role=Role.TEACHER)
    staff = User(id=3, username='staff1', password=generate_password_hash('staff123'), role=Role.STAFF)
    db.session.add_all([admin, teacher, staff])
    db.session.add_all([Admin(id=1), Teacher(id=2, name='Nguyễn Văn A', subject_id=subjects[0].id), Staff(id=3)])

    # --- Học kỳ ---
    db.session.add_all([Semester(name='Học kỳ 1'), Semester(name='Học kỳ 2')])

    # --- Lớp học (2 lớp mỗi khối) ---
    class_map = {}
    for grade in [grade10, grade11, grade12]:
        class_map[grade.id] = []
        for i in range(1, 3):  # A1, A2
            c = Classroom(name=f"{grade.name.value}A{i}", gradelevel_id=grade.id, academic_year="2024-2025")
            db.session.add(c)
            db.session.flush()
            class_map[grade.id].append(c)

    # //--- Tạo dữ liệu giả cho 30 học sinh mỗi khối, không phân lớp tự động
    students = []
    for grade in [grade10, grade11, grade12]:
        for _ in range(30):
            s = Student(
                name=fake.name(),
                gender=random.choice([Gender.MALE, Gender.FEMALE]),
                birth_date=fake.date_of_birth(minimum_age=15, maximum_age=20),
                address=fake.address(),
                phone=fake.phone_number(),
                email=fake.email(),
                grade_id=grade.id,
                classroom_id=None  # Không gán lớp
            )
            students.append(s)

    db.session.add_all(students)

    # --- Phụ huynh mẫu ---
    db.session.add_all([
        Parent(name=fake.name(), phone=fake.phone_number(), relation=Relationship.FATHER, student=students[0]),
        Parent(name=fake.name(), phone=fake.phone_number(), relation=Relationship.MOTHER, student=students[1]),
    ])

    db.session.commit()
    print("✅ Cơ sở dữ liệu và dữ liệu mẫu đã được khởi tạo thành công.")
