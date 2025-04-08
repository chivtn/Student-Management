from StudentManagementApp.models import *
from StudentManagementApp import app, db, dao, utils
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request,render_template


class AuthenticatedAdmin(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class Authenticated_Admin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class StatsView(AuthenticatedAdmin):
    @expose("/")
    def index(self):

        return self.render('admin/Statistics.html', subjects=dao.get_subject(), semesters=dao.get_semester())


class ChangeRule(AuthenticatedAdmin):
    @expose("/")
    def index(self):

        return self.render('admin/ChangeRule.html', quantity=app.config['soluong'],
                           min_age=app.config['mintuoi'], max_age=app.config['maxtuoi'])


class SubjectView(Authenticated_Admin):
    column_list=['id_subject', 'name_subject']
    column_searchable_list = ['name_subject']
    column_filters = ['id_subject', 'name_subject']
    column_editable_list = ['name_subject']
    edit_modal = True
    can_export = True

class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')

class AdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        total_users = User.query.count()
        total_subjects = Subject.query.count()
        total_classes = Class.query.count()
        total_teachers = User.query.filter_by(user_role=UserRoleEnum.TEACHER).count()

        return self.render('admin/index.html',
                           total_users=total_users,
                           total_subjects=total_subjects,
                           total_classes=total_classes,
                           total_teachers=total_teachers,

                           )
admin = Admin(app=app, name='Quản lý học sinh', template_mode='bootstrap4', index_view=AdminIndex(name='Trang chủ'))

admin._index_view = AdminIndex(name='Trang chủ')

admin.add_view(SubjectView(Subject, db.session, name='Quản lý môn học'))
admin.add_view(StatsView(name='Thống kê báo cáo'))
admin.add_view(ChangeRule(name='Thay đổi quy định'))
admin.add_view(LogoutView(name='Đăng xuất'))