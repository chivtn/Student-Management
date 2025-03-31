from StudentManagementApp.models import *
from StudentManagementApp import app
import hashlib
from sqlalchemy import func
from flask import jsonify

if __name__ == '__main__':
    with app.app_context():
        print(statistics_subject(1,1,1))
