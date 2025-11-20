## 🎓 Student Management System

High School Student Management Web Application

## 📚 Table of Contents

📘 Introduction

🛠️ Technologies Used

👥 System Roles

🧩 System Features

🗄️ Database Overview

🏆 Achievements

🚀 Installation Guide

👨‍💻 Contributors

## 📘 Introduction

The Student Management System is a web-based platform designed for high schools to manage:

📝 Student enrollment

🏫 Class distribution & adjustment

🧮 Grade entry & GPA calculation

📤 Grade export

📊 Academic reports & charts

📚 Subject management

⚙️ Regulation updates

The system helps automate workflows, reduce manual tasks, and ensure accurate academic data for staff, teachers, and administrators.

## 🛠️ Technologies Used

You may adjust depending on your actual project.

🔧 Backend: Flask / Python

🎨 Frontend: HTML, CSS, JavaScript

🗃️ Database: MySQL / SQLite

📈 Libraries: Chart.js, ExcelJS

📤 File Export: Excel (with password protection)

🧵 Database Interaction: SQL

## 👥 System Roles
```bash
🧑‍💼 Staff

📝 Register new students

📋 View class lists

🔄 Adjust class assignments

🔍 Search & filter students

👨‍🏫 Teacher

✏️ Enter grades

💾 Save draft or finalize

🧮 Auto GPA calculation

📤 Export grades to Excel

🛠️ Administrator

📚 Manage subjects

⚙️ Update school regulations

📊 Access analytics & charts

📥 Export academic reports
```

## 🧩 System Features
```bash
1️⃣ Student Enrollment

Validate:

📧 Email format

📱 Phone number

🎂 Age requirement

🔍 Search & filter by grade level

❌ Delete students (if no grades exist)

2️⃣ Automatic Class Assignment

🏫 Auto-distribute students based on max class size

➕ Create new classes when needed

🔄 Auto-redistribute when regulations change

3️⃣ Class Adjustment

🎯 Select Grade → Class → Student

🔍 Search within class or entire system

🔁 Move student to a new class (same grade, not full)

📊 Auto-update class sizes

4️⃣ Grade Entry

Supports multiple score types:

🟦 15-minute tests

🟥 One-period tests

🟩 Final exam

Features:

🔢 Real-time GPA calculation

📝 Save as draft (editable)

🔐 Save as official (locked)

5️⃣ Grade Export

Export GPA based on:

🏫 Class

🗓️ Semester

📅 Academic Year

Includes:

📄 Excel file download

🔑 Password protection

👀 Preview in UI

6️⃣ Subject Management

🔍 Search subjects

➕ Add new subjects

✏️ Inline editing

❌ Delete subject

⚖️ Manage scoring weights (15-min, 1-period, final exam)

7️⃣ Regulation Management

👥 Max class size

🎂 Min/max student age

🧮 Score column limits

⚠️ Validation checks

🔄 Auto-redistribute if necessary

8️⃣ Reporting & Statistics

Filter by:

📚 Subject

🗓️ Semester

📅 Academic Year

Results include:

👥 Class size

🟩 Number of students passing

📊 Pass rate

Charts (Chart.js):

📈 Bar

🟦 Column

🟪 Pie

Exportable to Excel.
```

## 🗄️ Database Overview

The system includes 19 relational tables, such as:

👤 User, Teacher, Staff, Admin

🎓 Student, Classroom, GradeLevel

📚 Subject

📝 ScoreSheet, ScoreDetail, DraftScore

🗓️ AcademicYear, Semester

⚙️ Regulation

🔢 Enum Tables: Gender, ScoreType, Role, Grade

🔗 N–N Table: Teacher_Classroom

Supports:

1️⃣ One-to-One

💠 One-to-Many

🔁 Many-to-Many

🧩 Composition

🧬 Inheritance

## 🏆 Achievements

✔️ Fully implemented all project requirements

✔️ Intuitive interface for all roles

✔️ Smart class assignment and redistribution

✔️ Accurate grade management

✔️ Professional Excel export

✔️ Clean reporting and visualization

✔️ Extendable structure

## 🚀 Installation Guide
# Clone project
git clone <your-repo-url>

# Install dependencies
pip install -r requirements.txt

# Run the system
python app.py

## 👨‍💻 Contributors
Student ID	Name
2254052042	Bùi Dạ Lý
2254050009	Huỳnh Lệ Giang
2254052008	Võ Thị Ngọc Chi
