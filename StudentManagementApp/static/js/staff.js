let selectedStudent = null;
let selectedClassId = null;

// ======= TÌM KIẾM HỌC SINH =======
function handleSearch() {
    const name = document.getElementById('searchInput').value;
    const gradeId = document.getElementById('filterGradeAdd').value;
    searchStudentAddStu(name, gradeId);
}

function showAllStudents() {
    const gradeId = document.getElementById('filterGradeAdd').value;
    searchStudentAddStu("", gradeId);
}

function searchStudentAddStu(name, gradeId) {
    fetch("/staff/api/searchStudentAddStu", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ searchstudentAddStu: name, grade_id: gradeId })
    })
    .then(res => res.json())
    .then(data => renderResults(data));
}

function renderResults(data) {
    const list = document.getElementById('list-student');
    const noResult = document.getElementById('no-results');

    list.innerHTML = '';
    noResult.style.display = data[0].quantity === 0 ? 'block' : 'none';

    for (let i = 1; i <= data[0].quantity; i++) {
        const s = data[i];
        list.innerHTML += `
            <tr data-student-id="${s.id}">
                <td>${i}</td>
                <td>${s.name}</td>
                <td>${s.sex}</td>
                <td>${s.DoB}</td>
                <td>${s.address}</td>
                <td>${s.email}</td>
                <td>${s.phonenumber}</td>
                <td>${s.grade}</td>
                <td><button class="btn btn-sm btn-danger" onclick="deleteStudent(${s.id})">Xóa</button></td>
            </tr>
        `;
    }
}

function deleteStudent(studentId) {
    if (confirm('Bạn chắc chắn muốn xóa học sinh này?')) {
        fetch(`/staff/api/deleteStudent/${studentId}`, { method: 'DELETE' })
            .then(res => res.json())
            .then(data => {
                if (data.success) showAllStudents();
                else alert(data.error || 'Xóa thất bại');
            })
            .catch(() => alert('Lỗi khi kết nối tới server!'));
    }
}

// ======= IN DANH SÁCH LỚP =======
function printClass(classId) {
    fetch("/staff/api/printClass", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_class: classId })
    })
    .then(res => res.json())
    .then(data => {
        const table = document.getElementById('table_print_class');
        const nameClass = document.getElementById('name_class');
        const quantity = document.getElementById('quantity');
        const alertBox = document.getElementById('no_student');
        const tableBox = document.getElementById('print_class');

        nameClass.textContent = `Lớp: ${data[0].class}`;
        quantity.textContent = `Sĩ số: ${data[0].quantity}`;

        if (data[0].quantity === 0) {
            alertBox.style.display = 'inline';
            tableBox.style.display = 'none';
            alertBox.innerHTML = `<div class="alert alert-info text-center">Lớp không có học sinh</div>`;
        } else {
            tableBox.style.display = 'inline';
            alertBox.style.display = 'none';

            // Xóa các dòng cũ
            while (table.rows.length > 1) table.deleteRow(1);

            for (let i = 1; i <= data[0].quantity; i++) {
                const row = table.insertRow();
                row.innerHTML = `
                    <td>${i}</td>
                    <td>${data[i].name}</td>
                    <td>${data[i].sex}</td>
                    <td>${data[i].DoB}</td>
                    <td>${data[i].address}</td>
                `;
            }
        }

        // Cập nhật số lượng trên nút
        const button = document.querySelector(`#btn-class-${classId}`);
        if (button) {
            button.setAttribute('data-student-count', data[0].quantity);
            button.textContent = `${data[0].class} (${data[0].quantity})`;
        }
    });
}

function handleClassButton(classId, btn) {
    document.querySelectorAll('.class-button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    printClass(classId);
}

document.addEventListener('DOMContentLoaded', () => {
    const firstBtn = document.querySelector('.class-button');
    if (firstBtn) handleClassButton(+firstBtn.id.replace('btn-class-', ''), firstBtn);
});

// ======= CHUYỂN LỚP =======
function loadClassesByGrade(gradeId) {
    const select = document.getElementById('filterClass');
    select.innerHTML = '<option value="">Chọn lớp</option>';
    if (!gradeId) return;

    fetch(`/staff/api/getClassesByGrade/${gradeId}`)
        .then(res => res.json())
        .then(classes => {
            classes.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id_class;
                opt.textContent = c.name_class;
                select.appendChild(opt);
            });
        });
}

function searchStudent() {
    const name = document.getElementById('searchstudent').value;
    const classId = document.getElementById('filterClass').value;

    fetch("/staff/api/searchStudent", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ searchstudent: name, class_id: classId })
    })
    .then(res => res.json())
    .then(data => {
        const result = document.getElementById("result_searchstudent");
        const noResult = document.getElementById("no_result_searchstudent");
        result.innerHTML = '';
        noResult.innerHTML = '';

        if (data[0].quantity === 0) {
            noResult.innerHTML = '<div class="alert alert-info">Không tìm thấy học sinh</div>';
        } else {
            for (let i = 1; i <= data[0].quantity; i++) {
                const s = data[i];
                result.innerHTML += `
                    <tr>
                        <td>${s.id}</td>
                        <td>${s.name}</td>
                        <td>${s.class}</td>
                        <td><button class="btn btn-sm btn-primary" onclick="selectStudent(${s.id}, '${s.name}', '${s.class}')">Chọn</button></td>
                    </tr>
                `;
            }
        }
    });
}

function selectStudent(id, name, className) {
    selectedStudent = { id, name, class: className };
    document.getElementById('studentName').innerText = `${name} (${className})`;
    document.getElementById('btnChangeClass').disabled = false;
}

function selectNewClass(classId, element) {
    if (element.classList.contains('disabled')) return;
    document.querySelectorAll('.class-option').forEach(btn => btn.classList.remove('active'));
    element.classList.add('active');
    selectedClassId = classId;
}

function changeClass() {
    if (!selectedStudent || !selectedClassId) {
        alert("Vui lòng chọn học sinh và lớp mới!");
        return;
    }

    fetch('/staff/change_class', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            student_id: selectedStudent.id,
            new_class_id: selectedClassId
        })
    })
    .then(res => res.json())
    .then(data => {
        const resultDiv = document.getElementById('changeClassResult');
        resultDiv.innerHTML = `<div class="alert alert-${data.success ? 'success' : 'danger'}">${data.message}</div>`;

        // Cập nhật lại sĩ số hiển thị cho lớp cũ và lớp mới
        const oldBtn = document.querySelector(`[data-class-id="${data.old_class.id}"]`);
        const newBtn = document.querySelector(`[data-class-id="${data.new_class.id}"]`);
        if (oldBtn) {
            oldBtn.textContent = `${data.old_class.name} (${data.old_class.current_student}/${data.max_per_class})`;
        }
        if (newBtn) {
            newBtn.textContent = `${data.new_class.name} (${data.new_class.current_student}/${data.max_per_class})`;
        }


        if (data.success) {
            resetSelection();
            searchStudent(); // Cập nhật lại danh sách
        }
    })
    .catch(() => alert("Có lỗi xảy ra khi kết nối đến server"));
}

function resetSelection() {
    document.getElementById('studentName').innerText = "Chưa chọn học sinh";
    document.getElementById('btnChangeClass').disabled = true;
    selectedStudent = null;
    selectedClassId = null;
    document.querySelectorAll('.class-option').forEach(btn => btn.classList.remove('active'));
}
