from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'GHFGH&*%^$^*(JHFGHF&Y*R%^$%$^&*TGYGJHFHGVJHGY'

# ✅ Cấu hình kết nối database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:26032004@localhost/hocsinhdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# ✅ Giá trị mặc định nếu chưa có trong DB
app.config['soluong'] = 40
app.config['maxtuoi'] = 20
app.config['mintuoi'] = 15
app.config['nambatdau'] = 2025

# ✅ Khởi tạo các extension
db = SQLAlchemy(app=app)
login = LoginManager(app=app)
login.login_view = 'login'

# ✅ Hàm load quy định từ DB vào app.config
def load_regulations():
    from StudentManagementApp.models import Regulation
    regulations = Regulation.query.all()
    for rule in regulations:
        name = rule.name_regulations.lower()
        if "số lượng" in name:
            app.config['soluong'] = rule.value_regulations
        elif "nhỏ nhất" in name:
            app.config['mintuoi'] = rule.value_regulations
        elif "lớn nhất" in name:
            app.config['maxtuoi'] = rule.value_regulations

# ✅ Tạo bảng và load dữ liệu nếu chạy trực tiếp
if __name__ == '__main__':
    from StudentManagementApp.models import Regulation

    with app.app_context():
        db.create_all()
        # Load vào app.config
        load_regulations()
        print("✅ Đã load quy định từ database vào app.config.")
