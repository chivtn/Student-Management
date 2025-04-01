from .enums import KhoiLop

class MonHoc:
    def __init__(self, idMH, tenMH, soCotDiem15P, soCotDiem1Tiet, khoi: KhoiLop):
        self.idMH = idMH
        self.tenMH = tenMH
        self.soCotDiem15P = soCotDiem15P
        self.soCotDiem1Tiet = soCotDiem1Tiet
        self.khoi = khoi