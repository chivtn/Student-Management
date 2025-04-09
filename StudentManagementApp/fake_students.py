from StudentManagementApp import app, db
from StudentManagementApp.models import Student, Class, Grade, Sex
from faker import Faker
import random
from datetime import datetime

fake = Faker('vi_VN')  # Sử dụng tiếng Việt


def create_fake_students():
    with app.app_context():
        # Lấy tất cả các lớp từ CSDL
        classes = Class.query.all()
        grades = Grade.query.all()

        # Số học sinh cần tạo (ví dụ: 200 học sinh)
        num_students = 800

        for _ in range(num_students):
            # Random thông tin học sinh
            name = fake.name()
            sex = random.choice([Sex.MALE, Sex.FEMALE])

            # Đảm bảo năm sinh hợp lệ (15-20 tuổi tính từ 2023)
            birth_year = 2025 - random.randint(15, 20)
            dob = fake.date_of_birth(minimum_age=15, maximum_age=20)

            address = fake.address()
            phonenumber = '0' + ''.join(random.choices('0123456789', k=9))
            email = f"{name.split()[-1].lower()}{random.randint(100, 999)}@gmail.com"

            # Chọn ngẫu nhiên 1 khối và lớp thuộc khối đó
            grade = random.choice(grades)
            class_options = [c for c in classes if c.id_grade == grade.id_grade]
            selected_class = random.choice(class_options)

            # Kiểm tra lớp chưa đầy (40 học sinh)
            if selected_class.current_student < 40:
                student = Student(
                    name=name,
                    sex=sex,
                    DoB=dob,
                    address=address,
                    phonenumber=phonenumber,
                    email=email,
                    id_grade=grade.id_grade,
                )
                db.session.add(student)

        db.session.commit()
        print("✅ Đã tạo dữ liệu giả thành công!")


if __name__ == '__main__':
    create_fake_students()