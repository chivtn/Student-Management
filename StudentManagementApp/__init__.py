

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
