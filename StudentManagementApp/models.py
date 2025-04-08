from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from StudentManagementApp import db, app
from flask_login import UserMixin
import enum
import hashlib


class UserRoleEnum(enum.Enum):
    ADMIN = 1
    STAFF = 2
    TEACHER = 3

class Sex(enum.Enum):
    MALE= "NAM"
    FEMALE = "NU"

class Grade_Enum(enum.Enum):
    GRADE_10 = "10"
    GRADE_11 = "11"
    GRADE_12 = "12"

class Relationship(enum.Enum):
    DAD = "CHA"
    MOM = "ME"
    GUARDIAN = "NGUOI_GIAM_HO"

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRoleEnum), nullable=False)

    def __str__(self):
        return self.hoTen

    def get_id(self):
        return str(self.id)

# Khối Lớp
class Grade(db.Model):
    __tablename__ = 'Grade'
    id_grade = Column(Integer, primary_key=True, autoincrement=True)
    name_grade = Column(Enum(Grade_Enum), nullable=False)

    # Mỗi Khối Lớp có nhiều Lớp Học
    classes = relationship('Class', backref='grade', lazy=True)
    # Mỗi Khối Lớp có nhiều Học Sinh
    students = relationship('Student', backref='Grade', lazy=True)

# Lớp Học
class Class(db.Model):
    __tablename__ = 'Class'
    id_class = Column(Integer, primary_key=True, autoincrement=True)
    name_class = Column(String(50), nullable=False)

    @property
    def current_student(self):
        return len(self.students)  # Tự động tính số học sinh trong lớp

    # Mỗi Lớp Học thộc về 1 Khối Lớp
    id_grade = Column(Integer, ForeignKey(Grade.id_grade), nullable=False)
    # Mỗi Lớp Học có nhiều Học sinh
    students = relationship('Student', backref='Class', lazy=True)

    # # Mỗi Lớp Học có nhiều dạy Giáo viên
    # giaoViens = relationship('GiaoVien', backref='LopHoc', lazy=True)
    #
    # # Mỗi Lớp Học có 1 giáo viên chủ nhiệm
    # idGiaoVien = Column(Integer, ForeignKey('GiaoVien.idGV'), nullable=False)
    #
    # # Mỗi Lớp Học có nhiều Nhân Viên quản lý
    # nhanViens = relationship('Staff', backref='LopHoc', lazy=True)
    #
    # # Mỗi Lớp Học có nhiều Bảng điểm môn học
    # bangDiems = relationship('BangDiemMonHoc', backref='LopHoc', lazy=True)

# Học Sinh
class Student(db.Model):
    __tablename__ = 'Student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    sex = Column(Enum(Sex), nullable=False)
    DoB = Column(DateTime, nullable=False)
    address = Column(String(100), nullable=False)
    phonenumber = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)

    # Mỗi học sinh thuộc về 1 Lớp Học
    id_class = Column(Integer, ForeignKey(Class.id_class), nullable=True)
    # Mỗi Học Sinh thuộc về 1 khối
    id_grade = Column(Integer, ForeignKey(Grade.id_grade), nullable=False)
    # # Mỗi học sinh có nhiều phụ huynh
    # phuHuynhs = relationship('PhuHuynh', secondary='HocSinh_PhuHuynh', back_populates='hocSinhs')


# Học Kỳ
class Semester(db.Model):
    __tablename__ = 'Semester'
    id_semester = Column(Integer, primary_key=True, autoincrement=True)
    name_semester = Column(String(50), nullable=False)

# Môn Học
class Subject(db.Model):
    __tablename__ = 'Subject'
    id_subject = Column(Integer, primary_key=True, autoincrement=True)
    name_subject = Column(String(100), nullable=False)
    score15P_column_number = Column(Integer, nullable=True)
    score1T_column_number = Column(Integer, nullable=True)

# Phụ Huynh
class Parents(db.Model):
    __tablename__ = 'Parents'
    id_parents = Column(Integer, primary_key=True, autoincrement=True)
    name_parents = Column(String(50), nullable=False)
    phonenumber = Column(String(20), nullable=False)

    # Mỗi phụ huynh có nhiều học sinh (con của phụ huynh)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        u1 = User(name='Staff', username='staff',
                  password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.STAFF)
        db.session.add_all([u1])
        db.session.commit()

        grade1 = Grade(name_grade= Grade_Enum.GRADE_10)
        grade2 = Grade(name_grade= Grade_Enum.GRADE_11)
        grade3 = Grade(name_grade= Grade_Enum.GRADE_12)
        db.session.add_all([grade1, grade2, grade3])
        db.session.commit()

        c1 = Class(name_class='10A1', id_grade=1)
        c2 = Class(name_class='10A2', id_grade=1)
        c3 = Class(name_class='10A3', id_grade=1)
        c4 = Class(name_class='10A4', id_grade=1)
        c5 = Class(name_class='10A5', id_grade=1)
        # c6 = Class(name_class='10A6', id_grade=1)
        # c7 = Class(name_class='10A7', id_grade=1)
        # c8 = Class(name_class='10A8', id_grade=1)
        # c9 = Class(name_class='10A9', id_grade=1)
        # c10 = Class(name_class='10A10', id_grade=1)

        c11 = Class(name_class='11A1', id_grade=2)
        c12 = Class(name_class='11A2', id_grade=2)
        c13 = Class(name_class='11A3', id_grade=2)
        c14 = Class(name_class='11A4', id_grade=2)
        c15 = Class(name_class='11A5', id_grade=2)
        # c16 = Class(name_class='11A6', id_grade=2)
        # c17 = Class(name_class='11A7', id_grade=2)
        # c18 = Class(name_class='11A8', id_grade=2)
        # c19 = Class(name_class='11A9', id_grade=2)
        # c20 = Class(name_class='11A10', id_grade=2)

        c21 = Class(name_class='12A1', id_grade=3)
        c22 = Class(name_class='12A2', id_grade=3)
        c23 = Class(name_class='12A3', id_grade=3)
        c24 = Class(name_class='12A4', id_grade=3)
        c25 = Class(name_class='12A5', id_grade=3)
        # c26 = Class(name_class='12A6', id_grade=3)
        # c27 = Class(name_class='12A7', id_grade=3)
        # c28 = Class(name_class='12A8', id_grade=3)
        # c29 = Class(name_class='12A9', id_grade=3)
        # c30 = Class(name_class='12A10', id_grade=3)
        # c6, c7, c8, c9, c10, c16, c17, c18, c19, c20, c26, c27, c28, c29, c30
        db.session.add_all([c1, c2, c3, c4, c5,
                            c11, c12, c13, c14, c15,
                            c21, c22, c23, c24, c25, ])
        db.session.commit()

        s1 = Subject(name_subject="Ngữ văn")
        s2 = Subject(name_subject="Toán")
        s3 = Subject(name_subject="Ngoại ngữ")
        s4 = Subject(name_subject="Vật lý")
        s5 = Subject(name_subject="Hóa học")
        s6 = Subject(name_subject="Sinh học")
        s7 = Subject(name_subject="Lịch sử")
        s8 = Subject(name_subject="Địa lý")
        s9 = Subject(name_subject="Giáo dục công dân")
        s10 = Subject(name_subject="Tin học")
        s11 = Subject(name_subject="Giáo dục quốc phòng và an ninh")
        s12 = Subject(name_subject="Công nghệ")
        db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12])
        db.session.commit()

        s1 = Semester(name_semester="Học kỳ 1 năm học 2020-2021")
        s2 = Semester(name_semester="Học kỳ 2 năm học 2020-2021")
        s3 = Semester(name_semester="Học kỳ 1 năm học 2021-2022")
        s4 = Semester(name_semester="Học kỳ 2 năm học 2021-2022")
        s5 = Semester(name_semester="Học kỳ 1 năm học 2022-2023")
        s6 = Semester(name_semester="Học kỳ 2 năm học 2022-2023")
        s7 = Semester(name_semester="Học kỳ 1 năm học 2023-2024")
        s8 = Semester(name_semester="Học kỳ 2 năm học 2023-2024")
        db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8])
        db.session.commit()