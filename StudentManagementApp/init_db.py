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

    # --- Cấu hình quy định ---
    min_age = 15
    max_age = 20
    max_class_size = 40
    db.session.add(Regulation(min_age=min_age, max_age=max_age, max_class_size=max_class_size))

    # --- Môn học và Khối lớp ---
    grade10 = GradeLevel(id=1, name=Grade.GRADE_10)
    grade11 = GradeLevel(id=2, name=Grade.GRADE_11)
    grade12 = GradeLevel(id=3, name=Grade.GRADE_12)
    db.session.add_all([grade10, grade11, grade12])
    db.session.flush()

    subjects = [
        Subject(name="Toán", gradelevel=grade10),
        Subject(name="Ngữ văn", gradelevel=grade10),
        Subject(name="Tiếng Anh", gradelevel=grade10),
        Subject(name="Vật lý", gradelevel=grade11),
        Subject(name="Hóa học", gradelevel=grade11),
        Subject(name="Sinh học", gradelevel=grade11),
        Subject(name="Tin học", gradelevel=grade12),
        Subject(name="GDCD", gradelevel=grade12)
    ]
    db.session.add_all(subjects)
    db.session.flush()

    # --- Người dùng, phân quyền và giáo viên ---
    users = [
        User(id=1, username="admin", password=generate_password_hash("admin123"), role=Role.ADMIN),
        User(id=2, username="nguyenvangiang", password=generate_password_hash("teacher123"), role=Role.TEACHER),
        User(id=3, username="lethilan", password=generate_password_hash("staff123"), role=Role.STAFF)
    ]
    db.session.add_all(users)
    db.session.add(Admin(id=1))
    db.session.add(Staff(id=3))

    teacher = Teacher(id=2, name="Nguyễn Văn Giang", subject_id=subjects[0].id)
    db.session.add(teacher)
    db.session.flush()

    # --- Lớp học ---
    class_10A1 = Classroom(name="10A1", gradelevel=grade10, academic_year="2024-2025", homeroom_teacher=teacher)
    class_11A1 = Classroom(name="11A1", gradelevel=grade11, academic_year="2024-2025")
    class_12A1 = Classroom(name="12A1", gradelevel=grade12, academic_year="2024-2025")
    db.session.add_all([class_10A1, class_11A1, class_12A1])
    db.session.flush()

    teacher.classrooms.append(class_10A1)

    # --- Học kỳ ---
    db.session.add_all([
        Semester(name="Học kỳ 1"),
        Semester(name="Học kỳ 2")
    ])

    # --- Học sinh mẫu cho lớp 10A1 ---
    students = [
        Student(name=fake.name(), gender=random.choice([Gender.MALE, Gender.FEMALE]),
                birth_date=fake.date_of_birth(minimum_age=15, maximum_age=20),
                address=fake.address(), phone=fake.phone_number(),
                email=fake.email(), classroom_id=class_10A1.id, grade_id=grade10.id)
        for _ in range(5)  # Chỉ tạo 5 học sinh mẫu để dễ kiểm tra
    ]
    db.session.add_all(students)
    db.session.flush()

    # --- Phụ huynh mẫu ---
    parents = [
        Parent(name=fake.name(), phone=fake.phone_number(), relation=Relationship.FATHER, student_id=students[0].id),
        Parent(name=fake.name(), phone=fake.phone_number(), relation=Relationship.MOTHER, student_id=students[1].id)
    ]
    db.session.add_all(parents)

    db.session.commit()
    print("✅ Cơ sở dữ liệu và dữ liệu mẫu đã được khởi tạo thành công")
