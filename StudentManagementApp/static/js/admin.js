let myChart = null;
let resultData = {};

function statisticsScore() {
    const semesterId = document.getElementById('id_semester').value;
    const subjectId = document.getElementById('id_subject').value;

    fetch("/api/statisticsScore", {
        method: "POST",
        body: JSON.stringify({
            'id_semester': semesterId,
            'id_subject': subjectId
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        if (!res.ok) throw new Error('Network response was not ok');
        return res.json();
    }).then(function(data) {
        if (!data || data.length === 0) throw new Error('No data received');

        document.getElementById('result').style.display = 'block';
        document.getElementById('subject').textContent = `Môn học: ${data[0].subject}`;
        document.getElementById('semester').textContent = `Học kỳ: ${data[0].semester}`;
        document.getElementById('schoolyear').textContent = `Năm học: ${data[0].schoolyear}`;

        const tableBody = document.getElementById('table_result');
        tableBody.innerHTML = '';
        resultData = data;

        for (let i = 1; i <= data[0].quantity; i++) {
            const row = tableBody.insertRow();
            row.insertCell().textContent = i;
            row.insertCell().textContent = data[i].class;
            row.insertCell().textContent = data[i].quantity_student;
            row.insertCell().textContent = data[i].quantity_passed;
            row.insertCell().textContent = `${data[i].rate}%`;
        }

        document.getElementById('no-data').style.display = 'none';
        drawChart();
    }).catch(function(error) {
        console.error('Error:', error);
        alert('Có lỗi xảy ra khi tải dữ liệu. Vui lòng thử lại.');
    });
}

function drawChart() {
    const ctx = document.getElementById('chart');
    const chartType = document.getElementById('select_chart').value;
    document.getElementById('no-data').style.display = 'none';

    if (myChart) myChart.destroy();
    if (!resultData || resultData.length === 0) {
        document.getElementById('no-data').style.display = 'flex';
        return;
    }

    const labels = [];
    const dataValues = [];
    const backgroundColors = [];

    for (let i = 1; i <= resultData[0].quantity; i++) {
        labels.push(resultData[i].class);
        dataValues.push(resultData[i].quantity_passed);

        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        backgroundColors.push(`rgba(${r}, ${g}, ${b}, 0.7)`);
    }

    myChart = new Chart(ctx, {
        type: chartType,
        data: {
            labels: labels,
            datasets: [{
                label: 'Số lượng đạt',
                data: dataValues,
                backgroundColor: backgroundColors,
                borderColor: backgroundColors.map(color => color.replace('0.7', '1')),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) label += ': ';
                            if (context.parsed.y !== undefined) label += context.parsed.y;
                            return label;
                        }
                    }
                }
            }
        }
    });
}

function exportExcel() {
    const subjectText = document.getElementById('subject').textContent.replace('Môn học: ', '');
    const semesterText = document.getElementById('semester').textContent.replace('Học kỳ: ', '');
    const yearText = document.getElementById('schoolyear').textContent.replace('Năm học: ', '');

    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Báo cáo môn học');

    // ==== TIÊU ĐỀ LỚN ====
    worksheet.mergeCells('A1', 'E1');
    worksheet.getCell('A1').value = 'BÁO CÁO TỔNG KẾT MÔN HỌC';
    worksheet.getCell('A1').alignment = { horizontal: 'center' };
    worksheet.getCell('A1').font = { bold: true, size: 16 };

    // ==== THÔNG TIN MÔN HỌC ====
    worksheet.getCell('A3').value = `Môn: ${subjectText}`;
    worksheet.getCell('C3').value = `Học kỳ: ${semesterText}`;
    worksheet.getCell('A4').value = `Năm học: ${yearText}`;

    // ==== HEADER ====
    const headerRow = worksheet.addRow(['STT', 'Lớp', 'Sĩ số', 'Số lượng đạt', 'Tỷ lệ']);
    headerRow.font = { bold: true };
    headerRow.alignment = { horizontal: 'center' };
    headerRow.eachCell(cell => {
        cell.border = {
            top: { style: 'thin' },
            left: { style: 'thin' },
            bottom: { style: 'thin' },
            right: { style: 'thin' }
        };
        cell.fill = {
            type: 'pattern',
            pattern: 'solid',
            fgColor: { argb: 'FFD6EAF8' }
        };
    });

    // ==== DỮ LIỆU BẢNG ====
    const table = document.getElementById('table_result');
    const rows = table.rows;

    for (let i = 0; i < rows.length; i++) {
        const rowData = [];
        for (let j = 0; j < rows[i].cells.length; j++) {
            rowData.push(rows[i].cells[j].textContent);
        }
        const dataRow = worksheet.addRow(rowData);
        dataRow.alignment = { horizontal: 'center' };
        dataRow.eachCell(cell => {
            cell.border = {
                top: { style: 'thin' },
                left: { style: 'thin' },
                bottom: { style: 'thin' },
                right: { style: 'thin' }
            };
        });
    }

    // ==== TỰ ĐỘNG CĂN ĐỀU CỘT ====
    worksheet.columns.forEach(column => {
        column.width = 15;
    });

    // ==== XUẤT FILE ====
    workbook.xlsx.writeBuffer().then((data) => {
        const blob = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        saveAs(blob, `bao_cao_tong_ket_mon_${subjectText.replace(/\s+/g, '_')}.xlsx`);
    });
}


function changeRule(){
        const quantity = document.getElementById('quantity').value;
        const minAge = document.getElementById('min_age').value;
        const maxAge = document.getElementById('max_age').value;

        // Validate input
        if (minAge >= maxAge) {
            document.getElementById('result').innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle"></i> Tuổi nhỏ nhất phải nhỏ hơn tuổi lớn nhất
                </div>
            `;
            return;
        }

        fetch("/api/changeRule", {
            method: "post",
            body: JSON.stringify({
                "quantity": quantity,
                "min_age": minAge,
                "max_age": maxAge
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(res) {
            return res.json();
        }).then(function(data) {
            const result = document.getElementById('result');
            if(data.status === 200) {
                result.innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i> ${data.content}
                    </div>
                `;

                // Update current rules display
                document.getElementById('current-quantity').textContent = quantity;
                document.getElementById('current-min-age').textContent = minAge;
                document.getElementById('current-max-age').textContent = maxAge;


                // Clear message after 3 seconds
                setTimeout(() => {
                    result.innerHTML = '';
                }, 3000);
            } else {
                result.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-circle"></i> ${data.content}
                    </div>
                `;
            }
        }).catch(error => {
            document.getElementById('result').innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle"></i> Có lỗi xảy ra khi cập nhật quy định
                </div>
            `;
            console.error('Error:', error);
        });
    }