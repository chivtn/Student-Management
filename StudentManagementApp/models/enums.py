from enums import Enum

class VaiTro(Enum):
    QUAN_TRI_VIEN = "QUAN_TRI_VIEN"
    GIAO_VIEN = "GIAO_VIEN"
    NHAN_VIEN = "NHAN_VIEN"

class GioiTinh(Enum):
    NAM = "NAM"
    NU = "NU"

class LoaiDiem(Enum):
    DIEM_15_PHUT = "15P"
    DIEM_1_TIET = "1TIET"
    DIEM_CUOI_KY = "THI"

class KhoiLop(Enum):
    LOP_10 = "10"
    LOP_11 = "11"
    LOP_12 = "12"

class QuanHe(Enum):
    CHA = "CHA"
    ME = "ME"
    NGUOI_GIAM_HO = "NGUOI_GIAM_HO"