#init_db.py
from StudentManagementApp import create_app, db
from StudentManagementApp.models import *
from StudentManagementApp.models.enums import Role, Gender, ScoreType, Grade, Relationship
from werkzeug.security import generate_password_hash
from datetime import date

app = create_app()

with app.app_context():
    # Xóa toàn bộ bảng cũ và tạo lại
    db.drop_all()
    db.create_all()

    # --- Người dùng và phân quyền ---
    users = [
        User(id=1, username="admin", password=generate_password_hash("admin123"), role=Role.ADMIN),
        User(id=2, username="teacher1", password=generate_password_hash("teacher123"), role=Role.TEACHER),
        User(id=3, username="staff1", password=generate_password_hash("staff123"), role=Role.STAFF),
    ]
    db.session.add_all(users)
    db.session.flush()

    db.session.add(Admin(id=1))
    db.session.add(Staff(id=3))

    # --- Khối lớp ---
    grade10 = GradeLevel(id=1, name=Grade.GRADE_10)
    grade11 = GradeLevel(id=2, name=Grade.GRADE_11)
    grade12 = GradeLevel(id=3, name=Grade.GRADE_12)
    db.session.add_all([grade10, grade11, grade12])

    # --- Môn học ---
    subject_math = Subject(name="Toán", gradelevel=grade10)
    subject_lit = Subject(name="Ngữ văn", gradelevel=grade10)
    subject_phys = Subject(name="Vật lý", gradelevel=grade11)
    db.session.add_all([subject_math, subject_lit, subject_phys])
    db.session.flush()

    # --- Giáo viên ---
    teacher = Teacher(id=2, subject_id=subject_math.id)
    db.session.add(teacher)

    # --- Lớp học ---
    class_10a1 = Classroom(name="10A1", gradelevel=grade10, academic_year="2024-2025", homeroom_teacher=teacher)
    class_11b1 = Classroom(name="11B1", gradelevel=grade11, academic_year="2024-2025")
    class_12c1 = Classroom(name="12C1", gradelevel=grade12, academic_year="2024-2025")
    db.session.add_all([class_10a1, class_11b1, class_12c1])
    db.session.flush()

    # Gán giáo viên dạy các lớp
    teacher.classrooms.extend([class_10a1, class_11b1])

    # --- Học kỳ ---
    db.session.add_all([
        Semester(name="Học kỳ 1"),
        Semester(name="Học kỳ 2")
    ])

    # --- Quy định ---
    db.session.add(Regulation(min_age=15, max_age=20, max_class_size=40))

    # --- Học sinh lớp 10A1 ---
    students = [
        Student(full_name="Nguyễn Văn A", gender=Gender.MALE, birth_date=date(2008, 5, 10), address="Hà Nội", classroom=class_10a1),
        Student(full_name="Trần Thị B", gender=Gender.FEMALE, birth_date=date(2008, 7, 15), address="Hồ Chí Minh", classroom=class_10a1),
        Student(full_name="Lê Văn C", gender=Gender.MALE, birth_date=date(2007, 12, 20), address="Đà Nẵng", classroom=class_10a1),
        Student(full_name="Phạm Thị D", gender=Gender.FEMALE, birth_date=date(2009, 3, 5), address="Huế", classroom=class_10a1),
        Student(full_name="Hoàng Văn E", gender=Gender.MALE, birth_date=date(2007, 9, 25), address="Cần Thơ", classroom=class_10a1),
    ]
    db.session.add_all(students)
    db.session.flush()

    # --- Phụ huynh ---
    parents = [
        Parent(name="Nguyễn Văn Ba", phone="0901234567", relation=Relationship.FATHER, student_id=students[0].id),
        Parent(name="Trần Thị Mẹ", phone="0912345678", relation=Relationship.MOTHER, student_id=students[1].id),
    ]
    db.session.add_all(parents)

    db.session.commit()

    print("✅ Cơ sở dữ liệu đã được khởi tạo và thêm dữ liệu mẫu thành công!")
