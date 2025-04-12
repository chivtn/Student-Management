let quantity_student = 0
let quantity_student_in_class = 0
id_class = 0
let selectedStudent = null
let selectedClassId = null

// ✅ Thêm học sinh
function handleSearch() {
    const searchTerm = document.getElementById('searchInput').value;
    const gradeId = document.getElementById('filterGradeAdd').value;

    fetch("/staff/api/searchStudentAddStu", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ searchstudentAddStu: searchTerm, grade_id: gradeId })
    })
    .then(res => res.json())
    .then(data => renderResults(data));
}

function showAllStudents() {
    const gradeId = document.getElementById('filterGradeAdd').value;
    fetch("/staff/api/searchStudentAddStu", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ searchstudentAddStu: "", grade_id: gradeId })
    })
    .then(res => res.json())
    .then(data => renderResults(data));
}

function renderResults(data) {
    const resultList = document.getElementById('list-student');
    const noResultsDiv = document.getElementById('no-results');

    resultList.innerHTML = '';
    noResultsDiv.style.display = 'none';

    if (data[0].quantity === 0) {
        noResultsDiv.style.display = 'block';
    } else {
        for (let i = 1; i <= data[0].quantity; i++) {
            const student = data[i];
            resultList.innerHTML += `
                <tr data-student-id="${student.id}">
                    <td>${i}</td>
                    <td>${student.name}</td>
                    <td>${student.sex}</td>
                    <td>${student.DoB}</td>
                    <td>${student.address}</td>
                    <td>${student.email}</td>
                    <td>${student.phonenumber}</td>
                    <td>${student.grade}</td>
                    <td><button class="btn btn-sm btn-danger" onclick="deleteStudent(${student.id})">Xóa</button></td>
                </tr>
            `;
        }
    }
}

function deleteStudent(studentId) {
    if (confirm('Bạn chắc chắn muốn xóa học sinh này?')) {
        fetch(`/staff/api/deleteStudent/${studentId}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            if (data.success) showAllStudents();
            else alert(data.error || 'Xóa thất bại');
        })
        .catch(error => alert('Có lỗi xảy ra khi xóa học sinh'));
    }
}

function clearForm() {
    ['fullname', 'sex', 'DoB', 'address', 'email', 'phonenumber', 'grade']
        .forEach(id => document.getElementById(id).value = '');
}

function printClass(id) {
    fetch("/staff/api/printClass", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ id_class: id })
    })
    .then(res => res.json())
    .then(data => {
        id_class = data[0].id
        let a = document.getElementById('no_student')
        let b = document.getElementById('print_class')
        if(data[0].quantity == 0) {
            a.style.display = "inline"
            a.innerHTML = `<div class="alert alert-info text-center">Lớp không có học sinh</div>`
            b.style.display = "none"
        } else {
            document.getElementById('name_class').innerText = `Lớp: ${data[0].class}`
            document.getElementById('quantity').innerText = `Sĩ số: ${data[0].quantity}`
            a.style.display = "none"
            b.style.display = "inline"
            const table = document.getElementById('table_print_class')
            for(let i = 1; i <= quantity_student_in_class; i++) table.deleteRow(1)
            quantity_student_in_class = data[0].quantity
            for(let i = 1; i <= data[0].quantity; i++) {
                let row = table.insertRow()
                row.insertCell().innerText = i
                row.insertCell().innerText = data[i].name
                row.insertCell().innerText = data[i].sex
                row.insertCell().innerText = data[i].DoB
                row.insertCell().innerText = data[i].address
            }

        }
        const button = document.querySelector(`#btn-class-${id}`)
        if(button) {
            button.setAttribute('data-student-count', data[0].quantity)
            button.textContent = `${data[0].class} (${data[0].quantity})`
        }
    });
}

function handleClassButton(classId, buttonElement) {
    document.querySelectorAll('.class-button').forEach(btn => btn.classList.remove('active'))
    buttonElement.classList.add('active')
    printClass(classId)
}

document.addEventListener('DOMContentLoaded', () => {
    const firstClassButton = document.querySelector('.class-button')
    if(firstClassButton) handleClassButton(parseInt(firstClassButton.id.replace('btn-class-', '')), firstClassButton)
})

function loadClassesByGrade(gradeId) {
    const classSelect = document.getElementById('filterClass');
    classSelect.innerHTML = '<option value="">Chọn lớp</option>';
    if (!gradeId) return;
    fetch(`/staff/api/getClassesByGrade/${gradeId}`)
        .then(res => res.json())
        .then(classes => {
            classes.forEach(c => {
                const option = document.createElement('option');
                option.value = c.id_class;
                option.textContent = c.name_class;
                classSelect.appendChild(option);
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
                const row = `
                    <tr>
                        <td>${s.id}</td>
                        <td>${s.name}</td>
                        <td>${s.class}</td>
                        <td><button class="btn btn-sm btn-primary" onclick="selectStudent(${s.id}, '${s.name}', '${s.class}')">Chọn</button></td>
                    </tr>`;
                result.innerHTML += row;
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
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            student_id: selectedStudent.id,
            new_class_id: selectedClassId
        })
    })
    .then(res => res.json())
    .then(data => {
        const resultDiv = document.getElementById('changeClassResult');
        if (data.success) {
            resultDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
            document.getElementById('studentName').innerText = "Chưa chọn học sinh";
            document.getElementById('btnChangeClass').disabled = true;
            selectedStudent = null;
            selectedClassId = null;
            document.querySelectorAll('.class-option').forEach(btn => btn.classList.remove('active'));
            searchStudent();
        } else {
            resultDiv.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
        }
    })
    .catch(error => {
        alert("Có lỗi xảy ra khi kết nối đến server");
    });
}