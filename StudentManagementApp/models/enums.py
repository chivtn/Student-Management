from enum import Enum

class Role(Enum):
    ADMIN = "Quản trị viên"
    TEACHER = "Giáo viên"
    STAFF = "Nhân viên"

class Gender(Enum):
    MALE = "Nam"
    FEMALE = "Nữ"

class ScoreType(Enum):
    FIFTEEN_MIN = "Điểm 15 phút"
    ONE_PERIOD = "Điểm 1 tiết"
    FINAL = "Điểm thi"

class Grade(Enum):
    GRADE_10 = "Lớp 10"
    GRADE_11 = "Lớp 11"
    GRADE_12 = "Lớp 12"

class Relationship(Enum):
    FATHER = "Cha"
    MOTHER = "Mẹ"
    GUARDIAN = "Người giám hộ"

