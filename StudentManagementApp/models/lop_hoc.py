from .enums import KhoiLop

class LopHoc:
    def __init__(self, idLop, tenLop, khoi: KhoiLop, siSo):
        self.idLop = idLop
        self.tenLop = tenLop
        self.khoiLop = khoi
        self.siSo = siSo
        self.dsHocSinh = []
        self.gvChuNhiem = None

    def timHS(self):
        pass