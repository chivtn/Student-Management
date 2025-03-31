from StudentManagementApp.models import *
from StudentManagementApp import app, db, dao, utils
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request,render_template

# class AuthenticatedAdmin(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN
#
#
# class Authenticated_Admin(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN
#
# class AuthenticatedUser(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated

# class BaoCao(AuthenticatedAdmin):

# class ThayDoiQuyDinh(AuthenticatedAdmin):

# class QuanLyMonHoc(AuthenticatedAdmin):

# class QuanLyNguoiDung(AuthenticatedAdmin):

# class DangXuat(AuthenticatedAdmin):

# QuanTriVien.add_view(MyUserView(User, db.session))
# QuanTriVien.add_view(MyTeacherView(Teacher, db.session))
# QuanTriVien.add_view(MySubjectView(Subject, db.session))
# QuanTriVien.add_view(MyClassView(Class, db.session))
# QuanTriVien.add_view(BaoCao(name='Thống kê báo cáo'))
# QuanTriVien.add_view(ThayDoiQuyDinh(name='Thay đổi quy định'))
# QuanTriVien.add_view(DangXuat(name='Đăng xuất'))
