#init_db
from StudentManagementApp import app
from StudentManagementApp.models import *
from faker import Faker
from werkzeug.security import generate_password_hash
import random

fake = Faker('vi_VN')

with app.app_context():
    db.drop_all()
    db.create_all()

    # --- Quy định ---
    rule = Regulation(min_age=15, max_age=20, max_class_size=40)
    db.session.add(rule)

    # --- Năm học ---
    year_2024 = AcademicYear(start_year=2024, end_year=2025, is_active=True)
    db.session.add(year_2024)
    db.session.flush()

    # --- Khối lớp ---
    grade10 = GradeLevel(id=1, name=Grade.GRADE_10)
    grade11 = GradeLevel(id=2, name=Grade.GRADE_11)
    grade12 = GradeLevel(id=3, name=Grade.GRADE_12)
    db.session.add_all([grade10, grade11, grade12])
    db.session.flush()

    # --- Môn học ---
    subjects = [
        Subject(name="Toán", gradelevel=grade10, score15P_column_number=5, score1T_column_number=3),
        Subject(name="Văn", gradelevel=grade10, score15P_column_number=4, score1T_column_number=2),
        Subject(name="Anh", gradelevel=grade10, score15P_column_number=3, score1T_column_number=2),
        Subject(name="Lý", gradelevel=grade11, score15P_column_number=4, score1T_column_number=2),
        Subject(name="Hóa", gradelevel=grade11, score15P_column_number=4, score1T_column_number=2),
        Subject(name="Sinh", gradelevel=grade11, score15P_column_number=4, score1T_column_number=2),
        Subject(name="Tin", gradelevel=grade12, score15P_column_number=3, score1T_column_number=1),
        Subject(name="GDCD", gradelevel=grade12, score15P_column_number=2, score1T_column_number=1)
    ]
    db.session.add_all(subjects)
    db.session.flush()

    # --- Người dùng ---
    admin = User(id=1, name='Quản trị viên', username='admin', password=generate_password_hash('admin123'), role=Role.ADMIN)
    teacher = User(id=2, name='Giáo viên A', username='teacher1', password=generate_password_hash('teacher123'), role=Role.TEACHER)
    staff = User(id=3, name='Nhân viên B', username='staff1', password=generate_password_hash('staff123'), role=Role.STAFF)
    db.session.add_all([admin, teacher, staff])
    db.session.flush()

    db.session.add_all([
        Admin(id=admin.id),
        Teacher(id=teacher.id, subject_id=subjects[0].id),
        Staff(id=staff.id)
    ])
    db.session.flush()

    # --- Học kỳ ---
    semester1 = Semester(name='Học kỳ 1')
    semester2 = Semester(name='Học kỳ 2')
    db.session.add_all([semester1, semester2])
    db.session.flush()

    # --- Lớp học (2 lớp mỗi khối) ---
    class_map = {}
    for grade in [grade10, grade11, grade12]:
        class_map[grade.id] = []
        for i in range(1, 3):  # A1, A2
            c = Classroom(name=f"{grade.name.value}A{i}", gradelevel_id=grade.id, academic_year_id=year_2024.id)
            db.session.add(c)
            db.session.flush()
            class_map[grade.id].append(c)

    # --- Gán lớp cho giáo viên A ---
    teacher_obj = db.session.get(Teacher, 2)
    for c in class_map[grade10.id]:  # Dạy 2 lớp khối 10
        teacher_obj.classrooms.append(c)

    # --- Học sinh (40 mỗi khối, chia đều vào A1, A2) ---
    students = []
    for grade in [grade10, grade11, grade12]:
        for i in range(40):
            classroom = class_map[grade.id][i % 2]
            s = Student(
                name=fake.name(),
                gender=random.choice([Gender.MALE, Gender.FEMALE]),
                birth_date=fake.date_of_birth(minimum_age=15, maximum_age=20),
                address=fake.address(),
                phone=fake.phone_number(),
                email=fake.email(),
                classroom_id=classroom.id,
                grade_id=grade.id
            )
            students.append(s)
    db.session.add_all(students)
    db.session.flush()

    # --- ScoreSheet cho mỗi học sinh ---
    semesters = Semester.query.all()
    for student in students:
        for semester in semesters:
            for subject in subjects:
                if subject.gradelevel_id == student.grade_id:
                    sheet = ScoreSheet(
                        student_id=student.id,
                        subject_id=subject.id,
                        semester_id=semester.id,
                        academic_year_id=year_2024.id,
                        classroom_id=student.classroom_id
                    )
                    db.session.add(sheet)
    db.session.flush()

    # --- Điểm mẫu ---
    score_sheets = ScoreSheet.query.all()
    for sheet in score_sheets:
        db.session.add_all([
            ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.FIFTEEN_MIN, value=random.uniform(5, 10)),
            ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.FIFTEEN_MIN, value=random.uniform(4, 10)),
            ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.FIFTEEN_MIN, value=random.uniform(6, 10)),
            ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.ONE_PERIOD, value=random.uniform(5, 10)),
            ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.ONE_PERIOD, value=random.uniform(5, 9)),
            ScoreDetail(score_sheet_id=sheet.id, type=ScoreType.FINAL, value=random.uniform(5, 10)),
        ])

    db.session.commit()
    print("✅ Cơ sở dữ liệu và dữ liệu mẫu đã được khởi tạo thành công.")
