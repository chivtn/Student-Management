function calculateAverage(studentId) {
    let s15s = [...document.querySelectorAll(`#score15_${studentId} input`)]
        .map(i => parseFloat(i.value)).filter(n => !isNaN(n));
    let s1ts = [...document.querySelectorAll(`#score1tiet_${studentId} input`)]
        .map(i => parseFloat(i.value)).filter(n => !isNaN(n));
    let finalInput = document.querySelector(`[name='score_final_${studentId}']`);
    let final = finalInput ? parseFloat(finalInput.value) : NaN;

    const avgEl = document.getElementById(`avg_${studentId}`);
    if (s15s.length && s1ts.length && !isNaN(final)) {
        let avg15 = s15s.reduce((a, b) => a + b, 0) / s15s.length;
        let avg1t = s1ts.reduce((a, b) => a + b, 0) / s1ts.length;
        let avg = ((avg15 + avg1t * 2 + final * 3) / 6).toFixed(2);
        avgEl.textContent = avg;
    } else {
        avgEl.textContent = '-';
    }
}

// ============ THÊM ĐIỂM MỚI ============
window.addScoreInput = function (studentId, type) {
    const containerId = type === '15' ? `score15_${studentId}` : `score1tiet_${studentId}`;
    const container = document.getElementById(containerId);
    const max = parseInt(container.dataset.max, 10) || 0;

    const currentCount = container.querySelectorAll('input').length;
    if (currentCount >= max) {
        alert(`Không thể nhập quá ${max} điểm ${type === '15' ? '15 phút' : '1 tiết'}`);
        return;
    }

    const input = document.createElement("input");
    input.type = "number";
    input.step = "0.1";
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

// ============ TỰ TÍNH TOÁN LÚC LOAD ============
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.score-input').forEach(input => {
        input.addEventListener('input', e => {
            const studentId = e.target.name.split('_')[2];
            calculateAverage(studentId);
        });
    });
});
