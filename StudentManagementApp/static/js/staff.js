let quantity_student = 0
let quantity_student_in_class = 0
id_class = 0
let selectedStudent = null

// ✅ Giao diện Thêm học sinh
function searchStudentAddStu() {
    const searchTerm = document.getElementById('searchInput').value;
    const gradeId = document.getElementById('filterGradeAdd').value; // Lấy giá trị khối

    fetch("/api/searchStudentAddStu", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            searchstudentAddStu: searchTerm,
            grade_id: gradeId // Thêm grade_id vào request body
        })
    })
    .then(res => res.json())
    .then(data => {
        const originalList = document.getElementById('list-student');
        const resultList = document.getElementById('search-results');
        const noResultsDiv = document.getElementById('no-results');

        // Ẩn danh sách gốc
        originalList.style.display = 'none';

        // Xóa kết quả cũ
        resultList.innerHTML = '';

        if (data[0].quantity === 0) {
            noResultsDiv.style.display = 'block';
            resultList.style.display = 'none';
        } else {
            noResultsDiv.style.display = 'none';
            resultList.style.display = 'table-row-group';

            // Thêm kết quả mới
            for (let i = 1; i <= data[0].quantity; i++) {
                const student = data[i];
                resultList.innerHTML += `
                    <tr>
                        <td>${i}</td>
                        <td>${student.name}</td>
                        <td>${student.sex}</td>
                        <td>${student.DoB}</td>
                        <td>${student.address}</td>
                        <td>${student.email}</td>
                        <td>${student.phonenumber}</td>
                        <td>${student.grade}</td>
                        <td>
                            <button class="btn btn-sm btn-danger"
                                    onclick="deleteStudent(${student.id})">
                                Xóa
                            </button>
                        </td>
                    </tr>
                `;
            }
        }
    })
    .catch(error => console.error('Lỗi:', error));
}

function loadStudents() {
    fetch("/api/getStudents")
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById('list-student');
            tbody.innerHTML = ''; // Xóa dữ liệu cũ

            data.forEach((student, index) => {
                const row = `
                    <tr data-student-id="${student.id}">
                        <td>${index + 1}</td>
                        <td class="editable" data-field="name">${student.name}</td>
                        <td class="editable" data-field="sex">${student.sex}</td>
                        <td class="editable" data-field="DoB">${student.DoB}</td>
                        <td class="editable" data-field="address">${student.address}</td>
                        <td class="editable" data-field="email">${student.email}</td>
                        <td class="editable" data-field="phonenumber">${student.phonenumber}</td>
                        <td class="editable" data-field="grade">${student.grade}</td>
                        <td>
                            <button class="btn btn-sm btn-danger" onclick="deleteStudent(${student.id})">Xóa</button>
                        </td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        });
}

function deleteStudent(studentId) {
    if (confirm('Bạn chắc chắn muốn xóa học sinh này?')) {
        fetch(`/api/deleteStudent/${studentId}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Lỗi khi xóa học sinh');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Xóa hàng khỏi bảng
                const row = document.querySelector(`tr[data-student-id="${studentId}"]`);
                if (row) {
                    row.remove();
                    alert('Xóa thành công!');
                }
            } else {
                alert(data.error || 'Xóa thất bại');
            }
        })
        .catch(error => {
            console.error('Lỗi:', error);
            alert('Có lỗi xảy ra khi xóa học sinh');
        });
    }
}

// Làm trống Form
function clearForm() {
    document.getElementById('fullname').value = '';
    document.getElementById('sex').value = '';
    document.getElementById('DoB').value = '';
    document.getElementById('address').value = '';
    document.getElementById('email').value = '';
    document.getElementById('phonenumber').value = '';
    document.getElementById('grade').value = '';
}

function loadStudentsByGrade() {
    const gradeId = document.getElementById('filterGradeAdd').value;
    searchStudentAddStu(); // Gọi lại hàm tìm kiếm
}

// ✅ Giao diện Lập danh sách lớp
function printClass(id) {
    fetch("/api/printClass", {
        method: "post",
        body: JSON.stringify({
            "id_class" : id,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        id_class = data[0].id
        let a = document.getElementById('no_student')
        let b = document.getElementById('print_class')
        if(data[0].quantity == 0)
        {
            a.style.display = "inline"
            a.innerHTML = `<div class="alert alert-info text-center">Lớp không có học sinh</div>`
            b.style.display = "none"
        }
        else
        {
            let name_class = document.getElementById('name_class')
            name_class.innerText = `Lớp: ${data[0].class}`
            let quantity = document.getElementById('quantity')
            quantity.innerText = `Sĩ số: ${data[0].quantity}`

            a.style.display = "none"
            b.style.display = "inline"
            let table = document.getElementById('table_print_class')

            for(let i = 1; i <= quantity_student_in_class; i++)
                table.deleteRow(1)

            quantity_student_in_class = data[0].quantity

            for(let i = 1; i <= data[0].quantity; i++)
            {
                var row = table.insertRow()
                row.insertCell().innerText = i
                row.insertCell().innerText = data[i].name
                row.insertCell().innerText = data[i].sex
                row.insertCell().innerText = data[i].DoB
                row.insertCell().innerText = data[i].address
            }
        }
        const button = document.querySelector(`#btn-class-${id}`);
        if(button) {
            button.setAttribute('data-student-count', data[0].quantity);
            button.textContent = `${data[0].class} (${data[0].quantity})`;
        }
    });
}

// Xử lý khi click nút lớp
function handleClassButton(classId, buttonElement) {
    // Remove active class từ tất cả các nút
    document.querySelectorAll('.class-button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Thêm active class cho nút được click
    buttonElement.classList.add('active');

    // Gọi hàm hiển thị danh sách lớp
    printClass(classId);
}

// Khởi tạo lớp đầu tiên khi trang load
document.addEventListener('DOMContentLoaded', () => {
    const firstClassButton = document.querySelector('.class-button');
    if(firstClassButton) {
        handleClassButton(
            parseInt(firstClassButton.id.replace('btn-class-', '')),
            firstClassButton
        );
    }
});


// ✅ Giao diện Chuyển lớp cho học sinh
function loadStudentsAdjust() {
    fetch("/api/getStudentsAdjust")
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector('studentList'); // Sửa ID tại đây
            tbody.innerHTML = ''; // Xóa dữ liệu cũ

            data.forEach((student, index) => {
                const row = `
                    <tr>
                        <td>${student.id}</td>
                        <td>${student.name}</td>
                        <td>${student.class || "Chưa có lớp"}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        })
        .catch(error => console.error('Lỗi:', error));
}


// Hàm chọn học sinh
function selectStudent(id, name, className) {
    selectedStudent = { id, name, class: className };
    document.getElementById('studentName').innerText = `${name} (${className})`;
    document.getElementById('btnChangeClass').disabled = false; // Kích hoạt nút chuyển lớp
}


//function changeClass() {
//    if (!selectedStudent) {
//        alert("Vui lòng chọn học sinh!");
//        return;
//    }
//
//    if (!selectedClassId) {
//        alert("Vui lòng chọn lớp mới!");
//        return;
//    }
//
//    fetch('/change_class', {
//        method: 'POST',
//        headers: {'Content-Type': 'application/json'},
//        body: JSON.stringify({
//            student_id: selectedStudent.id,
//            new_class_id: selectedClassId
//        })
//    })
//    .then(res => res.json())
//    .then(data => {
//        const resultDiv = document.getElementById('changeClassResult');
//        if (data.success) {
//            // Cập nhật lớp cũ
//            if (data.old_class.id) {
//                const oldClassBtn = document.querySelector(`.class-option[data-class-id="${data.old_class.id}"]`);
//                if (oldClassBtn) {
//                    oldClassBtn.textContent = `${data.old_class.name} (${data.old_class.current_student}/${max_per_class})`;
//                    if (data.old_class.current_student < max_per_class) {
//                        oldClassBtn.classList.remove('disabled');
//                    }
//                }
//            }
//
//            // Cập nhật lớp mới
//            const newClassBtn = document.querySelector(`.class-option[data-class-id="${data.new_class.id}"]`);
//            if (newClassBtn) {
//                newClassBtn.textContent = `${data.new_class.name} (${data.new_class.current_student}/${max_per_class})`;
//                if (data.new_class.current_student >= max_per_class) {
//                    newClassBtn.classList.add('disabled');
//                }
//            }
//
//            // Reset giao diện
//            resultDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
//            document.getElementById('studentName').innerText = "Chưa chọn học sinh";
//            document.getElementById('btnChangeClass').disabled = true;
//            selectedStudent = null;
//            selectedClassId = null;
//
//            // Xóa active class
//            document.querySelectorAll('.class-option').forEach(btn => btn.classList.remove('active'));
//        } else {
//            resultDiv.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
//        }
//    })
//    .catch(error => {
//        console.error('Lỗi:', error);
//        alert("Có lỗi xảy ra khi kết nối đến server");
//    });
//}

function changeClass() {
    if (!selectedStudent) {
        alert("Vui lòng chọn học sinh!");
        return;
    }

    if (!selectedClassId) {
        alert("Vui lòng chọn lớp mới!");
        return;
    }

    fetch('/change_class', {
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
            // ✅ Cập nhật lớp CŨ
            if (data.old_class?.id) {
                const oldClassBtn = document.querySelector(`button[data-class-id="${data.old_class.id}"]`);
                if (oldClassBtn) {
                    // Cập nhật số lượng và trạng thái
                    const newCount = data.old_class.current_student;
                    const max = data.max_per_class; // Lấy từ response
                    oldClassBtn.textContent = `${data.old_class.name} (${newCount}/${max})`;
                    oldClassBtn.classList.toggle('disabled', newCount >= max);
                }
            }

            // ✅ Cập nhật lớp MỚI
            const newClassBtn = document.querySelector(`button[data-class-id="${data.new_class.id}"]`);
            if (newClassBtn) {
                const newCount = data.new_class.current_student;
                const max = data.max_per_class;
                newClassBtn.textContent = `${data.new_class.name} (${newCount}/${max})`;
                newClassBtn.classList.toggle('disabled', newCount >= max);
            }

            // ✅ Cập nhật danh sách học sinh (không cần load lại trang)
            searchStudent(); // Gọi lại hàm tìm kiếm để load danh sách mới

            // ✅ Reset giao diện
            resultDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
            document.getElementById('studentName').innerText = "Chưa chọn học sinh";
            document.getElementById('btnChangeClass').disabled = true;
            selectedStudent = null;
            selectedClassId = null;

            // ✅ Xóa active class
            document.querySelectorAll('.class-option').forEach(btn => btn.classList.remove('active'));
        } else {
            resultDiv.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
        }
    })
    .catch(error => {
        console.error('Lỗi:', error);
        alert("Có lỗi xảy ra khi kết nối đến server");
    });
}

function selectNewClass(classId, element) {
    // Kiểm tra nếu lớp đã đầy
    if (element.classList.contains('disabled')) return;

    // Xóa active class từ tất cả các nút
    document.querySelectorAll('.class-option').forEach(btn => {
        btn.classList.remove('active');
    });

    // Thêm active class cho nút được chọn
    element.classList.add('active');
    selectedClassId = classId;
}

// Hàm load lớp theo khối
function loadClassesByGrade(gradeId) {
    const classSelect = document.getElementById('filterClass');
    classSelect.innerHTML = '<option value="">Chọn lớp</option>';

    if (!gradeId) return;

    fetch(`/api/getClassesByGrade/${gradeId}`)
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

// Hàm tìm kiếm học sinh
function searchStudent() {
    const searchQuery = document.getElementById('searchstudent').value;
    const classId = document.getElementById('filterClass').value;
    fetch("/api/searchStudent", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            searchstudent: searchQuery,
            class_id: classId
        })
    })
    .then(res => res.json())
    .then(data => {
        const resultContainer = document.getElementById('result_searchstudent');
        resultContainer.innerHTML = '';
        if (data[0].quantity === 0) {
            document.getElementById('no_result_searchstudent').innerHTML =
                '<div class="alert alert-info">Không tìm thấy học sinh</div>';
        } else {
            document.getElementById('no_result_searchstudent').innerHTML = '';
            for (let i = 1; i <= data[0].quantity; i++) {
                const student = data[i];
                const row = `
                    <tr>
                        <td>${student.id}</td>
                        <td>${student.name}</td>
                        <td>${student.class}</td>
                        <td>
                            <button class="btn btn-sm btn-primary"
                                onclick="selectStudent(${student.id}, '${student.name}', '${student.class}')">
                                Chọn
                            </button>
                        </td>
                    </tr>
                `;
                resultContainer.innerHTML += row;
            }
        }
    })
    .catch(error => console.error('Lỗi:', error));
}

// Chung
document.addEventListener('DOMContentLoaded', () => {
    loadStudents(); // Tự động tải danh sách khi trang web được mở
    loadStudentsAdjust();
});