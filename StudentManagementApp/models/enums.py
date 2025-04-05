from enum import Enum

class Role(Enum):
    ADMIN = "QUAN_TRI_VIEN"
    TEACHER = "GIAO_VIEN"
    STAFF = "NHAN_VIEN"

class Gender(Enum):
    MALE = "NAM"
    FEMALE = "NU"

class ScoreType(Enum):
    FIFTEEN_MIN = "15P"
    ONE_PERIOD = "1TIET"
    FINAL = "THI"

class Grade(Enum):
    GRADE_10 = "LOP_10"
    GRADE_11 = "LOP_11"
    GRADE_12 = "LOP_12"

class Relationship(Enum):
    FATHER = "CHA"
    MOTHER = "ME"
    GUARDIAN = "NGUOI_GIAM_HO"

