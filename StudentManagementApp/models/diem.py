from .enums import LoaiDiem

class Diem:
    def __init__(self, idDiem, loaiDiem: LoaiDiem, giaTri):
        self.idDiem = idDiem
        self.loaiDiem = loaiDiem
        self.giaTri = giaTri

    def capNhatDiem(self):
        pass