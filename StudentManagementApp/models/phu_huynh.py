from .enums import QuanHe

class PhuHuynh:
    def __init__(self, idPH, hoTen, soDT, quanHe: QuanHe):
        self.idPH = idPH
        self.hoTen = hoTen
        self.soDT = soDT
        self.quanHeVoHS = quanHe