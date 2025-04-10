
function addScoreInput(studentId, type) {
    const container = document.getElementById(`score${type}_${studentId}`);
    const inputs = container.querySelectorAll('input');
    const max = type === '15' ? 5 : 3;
    if (inputs.length >= max) return;

    const input = document.createElement('input');
    input.type = 'number';
    input.name = `score_${type}_${studentId}_${inputs.length + 1}`;
    input.className = 'form-control mb-1 score-input';
    input.min = 0;
    input.max = 10;
    input.step = 0.1;
    input.addEventListener('input', () => calculateAverage(studentId));
    container.appendChild(input);
}

function calculateAverage(studentId) {
    let s15s = [...document.querySelectorAll(`#score15_${studentId} input`)]
        .map(i => parseFloat(i.value)).filter(n => !isNaN(n));
    let s1ts = [...document.querySelectorAll(`#score1tiet_${studentId} input`)]
        .map(i => parseFloat(i.value)).filter(n => !isNaN(n));
    let finalInput = document.querySelector(`[name='score_final_${studentId}']`);
    let final = finalInput ? parseFloat(finalInput.value) : NaN;

    if (s15s.length && s1ts.length && !isNaN(final)) {
        let avg15 = s15s.reduce((a, b) => a + b, 0) / s15s.length;
        let avg1t = s1ts.reduce((a, b) => a + b, 0) / s1ts.length;
        let avg = ((avg15 * 1 + avg1t * 2 + final * 3) / 6).toFixed(2);
        document.getElementById(`avg_${studentId}`).textContent = avg;
    } else {
        document.getElementById(`avg_${studentId}`).textContent = '-';
    }
}

// Automatically attach average calculation to existing inputs on page load
window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.score-input').forEach(input => {
        input.addEventListener('input', (e) => {
            const parts = e.target.name.split('_');
            const studentId = parts[2];
            calculateAverage(studentId);
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    window.addScoreInput = function (studentId, type) {
        const containerId = type === '15' ? `score15_${studentId}` : `score1tiet_${studentId}`;
        const container = document.getElementById(containerId);

        const timestamp = Date.now();
        const random = Math.floor(Math.random() * 100000);
        const uniqueKey = `score_${type}_${studentId}_${timestamp}_${random}`;

        const input = document.createElement("input");
        input.type = "number";
        input.name = uniqueKey;
        input.className = "form-control score-input";
        input.step = "0.1";
        input.min = "0";
        input.max = "10";

        const wrapper = document.createElement("div");
        wrapper.className = "d-flex align-items-center mb-1 gap-2";

        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.className = "btn btn-sm btn-outline-danger";
        removeBtn.textContent = "×";
        removeBtn.onclick = function () {
            wrapper.remove();
        };

        wrapper.appendChild(input);
        wrapper.appendChild(removeBtn);
        container.appendChild(wrapper);
    };
});

