import math
from flask import render_template, request, redirect, session, jsonify
import dao, utils
from StudentManagementApp import app, login, admin
from flask_login import login_user, current_user, logout_user, login_required
import cloudinary.uploader

@app.route("/")
def index():
    return render_template('layout/base.html')


if __name__ == "__main__":
    from StudentManagementApp import admin
    app.run(debug=True)