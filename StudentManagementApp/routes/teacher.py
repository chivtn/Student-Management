# routes/teacher.py
from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
from StudentManagementApp import db
from StudentManagementApp.models import Teacher, Classroom, Student, Subject, Semester
import pandas as pd
from io import BytesIO
from StudentManagementApp.dao import score_service

teacher = Blueprint('teacher', __name__, url_prefix='/teacher')

@teacher.route('/')
def index():
    teacher_id = 2  # giả định
    teacher = Teacher.query.get(teacher_id)
    return render_template('teacher/index.html', teacher=teacher)

@teacher.route('/avg_scores')
def view_avg_scores():
    teacher_id = 2  # sẽ thay bằng current_user.id sau
    selected_class = request.args.get('class_id', type=int)
    selected_year = request.args.get('year', default='2024-2025')
    selected_semester = request.args.get('semester', type=int)

    teacher_obj = Teacher.query.get(teacher_id)
    classes = teacher_obj.classrooms
    years = ['2023-2024', '2024-2025']
    semesters = Semester.query.all()
    scores_list = []

    if selected_class:
        students = Student.query.filter_by(classroom_id=selected_class).all()

        for student in students:
            if selected_semester:
                avg = score_service.calculate_avg_score(student.id, selected_year, selected_semester)
                scores_list.append({
                    "full_name": student.full_name,
                    "avg_score": round(avg, 2) if avg is not None else None
                })
            else:
                avg1 = score_service.calculate_avg_score(student.id, selected_year, 1)
                avg2 = score_service.calculate_avg_score(student.id, selected_year, 2)
                avg_year = round((avg1 + avg2) / 2, 2) if avg1 is not None and avg2 is not None else None
                scores_list.append({
                    "full_name": student.full_name,
                    "avg_score_sem1": round(avg1, 2) if avg1 is not None else None,
                    "avg_score_sem2": round(avg2, 2) if avg2 is not None else None,
                    "avg_score_year": avg_year
                })

    return render_template(
        'teacher/avg_scores.html',
        classes=classes,
        years=years,
        semesters=semesters,
        selected_class=selected_class,
        selected_year=selected_year,
        selected_semester=selected_semester,
        scores=scores_list
    )

@teacher.route('/export_avg_scores')
def export_avg_scores():
    class_id = request.args.get('class_id', type=int)
    year = request.args.get('year')
    semester = request.args.get('semester', type=int)

    students = Student.query.filter_by(classroom_id=class_id).all()
    data = []

    for student in students:
        if semester:
            avg = score_service.calculate_avg_score(student.id, year, semester)
            data.append({
                "Student": student.full_name,
                f"Semester {semester} Avg": round(avg, 2) if avg is not None else None
            })
        else:
            avg1 = score_service.calculate_avg_score(student.id, year, 1)
            avg2 = score_service.calculate_avg_score(student.id, year, 2)
            avg_year = round((avg1 + avg2) / 2, 2) if avg1 is not None and avg2 is not None else None
            data.append({
                "Student": student.full_name,
                "Semester 1 Avg": round(avg1, 2) if avg1 is not None else None,
                "Semester 2 Avg": round(avg2, 2) if avg2 is not None else None,
                "Year Avg": avg_year
            })

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Avg Scores')
    output.seek(0)

    filename = f'avg_scores_class_{class_id}_{year}.xlsx'
    return send_file(output, download_name=filename, as_attachment=True)

@teacher.route('/my_classes')
def view_classes():
    teacher_id = 2  # thay bằng current_user.id khi có đăng nhập
    teacher_obj = Teacher.query.get(teacher_id)
    classrooms = teacher_obj.classrooms
    return render_template('teacher/my_classes.html', classrooms=classrooms)

@teacher.route('/class/<int:class_id>')
def view_class_detail(class_id):
    classroom = Classroom.query.get_or_404(class_id)
    students = Student.query.filter_by(classroom_id=class_id).all()
    return render_template('teacher/class_detail.html', classroom=classroom, students=students)

@teacher.route('/enter_grades/<int:class_id>/<int:subject_id>/<int:semester_id>', methods=['GET', 'POST'])
def enter_grades(class_id, subject_id, semester_id):
    classroom = Classroom.query.get_or_404(class_id)
    subject = Subject.query.get_or_404(subject_id)
    semester = Semester.query.get_or_404(semester_id)
    students = Student.query.filter_by(classroom_id=class_id).all()
    academic_year = classroom.academic_year

    if request.method == 'POST':
        errors = score_service.save_quick_input_scores(
            students, request.form, subject.id, semester.id, academic_year
        )

        if errors:
            for e in errors:
                flash(e, 'danger')
        else:
            db.session.commit()
            flash("✅ Đã lưu điểm thành công!", "success")

        return redirect(url_for('teacher.enter_grades', class_id=class_id, subject_id=subject_id, semester_id=semester_id))

    return render_template('teacher/enter_grades.html',
                           classroom=classroom,
                           subject=subject,
                           semester=semester,
                           students=students)

@teacher.route('/select_for_grading', methods=['GET', 'POST'])
def select_for_grading():
    teacher_id = 2  # giả định hoặc dùng current_user.id khi triển khai thực tế
    teacher_obj = Teacher.query.get_or_404(teacher_id)
    classes = teacher_obj.classrooms
    semesters = Semester.query.all()

    selected_class = selected_semester = None
    students = []
    scores_map = {}
    message = None

    if request.method == 'POST':
        class_id = int(request.form['class_id'])
        semester_id = int(request.form['semester_id'])
        selected_class = Classroom.query.get_or_404(class_id)
        selected_semester = Semester.query.get_or_404(semester_id)
        academic_year = selected_class.academic_year
        subject_id = teacher_obj.subject.id

        students = Student.query.filter_by(classroom_id=class_id).all()

        if 'save_scores' in request.form:
            score_service.store_scores(
                request.form, students, academic_year, semester_id, teacher_obj.subject.id
            )
            db.session.commit()
            message = "✅ Đã lưu điểm chính thức!"

        elif 'draft' in request.form:
            score_service.save_draft_scores(
                request.form, students, academic_year, semester_id, teacher_obj.subject.id
            )
            db.session.commit()
            message = "💾 Đã lưu nháp"

        scores_map = score_service.fetch_scores_for_students(students, academic_year, semester_id, subject_id)

    return render_template(
        'teacher/select_grading.html',
        classes=classes,
        semesters=semesters,
        selected_class=selected_class,
        selected_semester=selected_semester,
        students=students,
        scores_map=scores_map,
        message=message
    )
