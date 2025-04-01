from .enums import GioiTinh

class HocSinh:
    def __init__(self, idHS, hoTen, ngaySinh, gioiTinh: GioiTinh, diaChi, soDT, email):
        self.idHS = idHS
        self.hoTen = hoTen
        self.ngaySinh = ngaySinh
        self.gioiTinh = gioiTinh
        self.diaChi = diaChi
        self.soDT = soDT
        self.email = email
        self.dsPhuHuynh = []
        self.lop = None