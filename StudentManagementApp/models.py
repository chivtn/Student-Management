from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from StudentManagementApp import db, app
from flask_login import UserMixin
import enum
import hashlib

class UserRoleEnum(enum.Enum):
    QuanTriVien = 1
    NhanVien = 2
    GiaoVien = 3

# Class NguoiDung

# Class QuanTriVien

# Class NhanVien

# Class GiaoVien

# Class HocSinh

# Class LopHoc

# Class MonHoc

# Class KhoiLop

# Class HocKy

# Class Diem

# Class LoaiDiem



