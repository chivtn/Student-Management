

from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'GHFGH&*%^$^*(JHFGHF&Y*R%^$%$^&*TGYGJHFHGVJHGY'

#Chi

# Cấu hình kết nối database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:26032004@localhost/hocsinhdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Giá trị mặc định nếu chưa có gì trong DB
app.config['soluong'] = 40
app.config['maxtuoi'] = 20
app.config['mintuoi'] = 15
app.config['nambatdau'] = 2025  # Năm học bắt đầu

# Khởi tạo các extension
db = SQLAlchemy(app=app)
login = LoginManager(app=app)
login.login_view = 'login'

# ✅ Đọc quy định từ bảng Regulation và gán vào app.config
def load_regulations():
    from StudentManagementApp.models import Regulation
    regulations = Regulation.query.all()
    for rule in regulations:
        if "số lượng" in rule.name_regulations.lower():
            app.config['soluong'] = rule.value_regulations
        elif "nhỏ nhất" in rule.name_regulations.lower():
            app.config['mintuoi'] = rule.value_regulations
        elif "lớn nhất" in rule.name_regulations.lower():
            app.config['maxtuoi'] = rule.value_regulations

# ✅ Tạo bảng và load quy định nếu chạy trực tiếp
if __name__ == '__main__':
    from StudentManagementApp.models import Regulation

    with app.app_context():
        db.create_all()

        # Chỉ thêm dữ liệu mặc định nếu chưa có
        if Regulation.query.count() == 0:
            r1 = Regulation(name_regulations="Quy định số lượng học sinh trong 1 lớp", value_regulations=40)
            r2 = Regulation(name_regulations="Quy định số tuổi nhỏ nhất của học sinh", value_regulations=15)
            r3 = Regulation(name_regulations="Quy định số tuổi lớn nhất của học sinh", value_regulations=20)
            db.session.add_all([r1, r2, r3])
            db.session.commit()
            print("✅ Đã tạo các quy định mặc định.")

        load_regulations()
        print("✅ Đã load các giá trị quy định vào app.config.")
