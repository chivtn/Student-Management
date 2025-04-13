// ✅ Tính điểm trung bình
function calculateAverage(studentId) {
    const inputs15 = document.querySelectorAll(`#score15_${studentId} input`);
    const inputs1tiet = document.querySelectorAll(`#score1tiet_${studentId} input`);
    const inputFinal = document.querySelector(`input[name='score_final_${studentId}']`);
    const avgSpan = document.getElementById(`avg_${studentId}`);

    let sum = 0, count = 0;

    inputs15.forEach(input => {
        const val = parseFloat(input.value);
        if (!isNaN(val)) {
            sum += val;
            count += 1;
        }
    });

    inputs1tiet.forEach(input => {
        const val = parseFloat(input.value);
        if (!isNaN(val)) {
            sum += val * 2;
            count += 2;
        }
    });

    if (inputFinal && inputFinal.value !== '') {
        const val = parseFloat(inputFinal.value);
        if (!isNaN(val)) {
            sum += val * 3;
            count += 3;
        }
    }

    if (count > 0) {
        const avg = (sum / count).toFixed(2);
        avgSpan.textContent = avg;
    } else {
        avgSpan.textContent = '-';
    }
}

//  Khi nhấn Lưu / Lưu nháp: Làm tròn toàn bộ điểm
document.addEventListener('submit', function (e) {
    if (e.target.tagName === 'FORM') {
        e.target.querySelectorAll('.score-input').forEach(input => {
            let val = parseFloat(input.value);
            if (!isNaN(val)) {
                input.value = val.toFixed(2);
            }
        });
    }
});

// Tự động tính lại trung bình khi người dùng nhập
document.addEventListener('input', function (e) {
    if (e.target.classList.contains('score-input')) {
        const studentId = e.target.name.split('_')[2];
        calculateAverage(studentId);
    }
});

// Thêm ô điểm mới
window.addScoreInput = function (studentId, type) {
    const containerId = type === '15' ? `score15_${studentId}` : `score1tiet_${studentId}`;
    const container = document.getElementById(containerId);
    const max = parseInt(container.dataset.max, 10) || 0;

    if (container.querySelectorAll('input').length >= max) {
        alert(`Không thể nhập quá ${max} điểm ${type === '15' ? '15 phút' : '1 tiết'}`);
        return;
    }

    const input = document.createElement("input");
    input.type = "number";
    input.step = "0.01";
    input.min = "0";
    input.max = "10";
    input.className = "form-control score-input";
    input.name = `score_${type}_${studentId}_${Date.now()}`;
    input.addEventListener('input', () => calculateAverage(studentId));

    const wrapper = document.createElement("div");
    wrapper.className = "d-flex align-items-center mb-1 gap-2";

    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "btn btn-sm btn-outline-danger";
    removeBtn.textContent = "×";
    removeBtn.onclick = () => {
        wrapper.remove();
        calculateAverage(studentId);
    };

    wrapper.appendChild(input);
    wrapper.appendChild(removeBtn);
    container.appendChild(wrapper);
};

// ✅ Khi load trang, tính trung bình ban đầu
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.score-input').forEach(input => {
        input.dispatchEvent(new Event('input'));
    });
});
