#_init_.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:askme@localhost:3306/studentdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login.init_app(app)

    # ✅ Đưa vào trong create_app để tránh vòng lặp
    from StudentManagementApp.models.user import User

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # import routes
    from StudentManagementApp.routes.teacher import teacher
    app.register_blueprint(teacher)

    return app
