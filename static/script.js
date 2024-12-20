const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const clearBtn = document.getElementById('clear-btn');
const predictBtn = document.getElementById('predict-btn');
const downloadBtn = document.getElementById('download-btn');
const result = document.getElementById('result');
const spinner = document.getElementById('spinner');
const themeToggle = document.getElementById('theme-toggle');
const brushColor = document.getElementById('brush-color');
const brushSize = document.getElementById('brush-size');

// Initialize canvas with white background
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

let drawing = false;
let color = '#000000';
let size = 10;

// Handle both mouse and touch events
function getPosition(event) {
    const rect = canvas.getBoundingClientRect();
    const clientX = event.touches ? event.touches[0].clientX : event.clientX;
    const clientY = event.touches ? event.touches[0].clientY : event.clientY;
    return {
        x: clientX - rect.left,
        y: clientY - rect.top
    };
}

function startDrawing(event) {
    event.preventDefault();
    drawing = true;
    const pos = getPosition(event);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
    draw(event);
}

function stopDrawing() {
    drawing = false;
    ctx.beginPath();
}

function draw(event) {
    if (!drawing) return;
    event.preventDefault();

    const pos = getPosition(event);
    ctx.lineWidth = size;
    ctx.lineCap = 'round';
    ctx.strokeStyle = color;

    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

// Mouse event listeners
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

// Touch event listeners
canvas.addEventListener('touchstart', startDrawing);
canvas.addEventListener('touchmove', draw);
canvas.addEventListener('touchend', stopDrawing);
canvas.addEventListener('touchcancel', stopDrawing);

// Theme toggle
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    themeToggle.textContent = document.body.classList.contains('dark-theme') 
        ? 'Light Mode' 
        : 'Dark Mode';
});

// Brush controls
brushColor.addEventListener('change', (e) => color = e.target.value);
brushSize.addEventListener('input', (e) => size = e.target.value);

// Clear canvas
clearBtn.addEventListener('click', () => {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    result.innerHTML = '';
});

// Predict digit
predictBtn.addEventListener('click', async () => {
    try {
        spinner.style.display = 'block';
        result.innerHTML = '';

        const imageData = canvas.toDataURL('image/png').split(',')[1];
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });

        const data = await response.json();
        
        if (data.error) {
            result.innerHTML = `<div class="error">Error: ${data.error}</div>`;
        } else {
            let resultsHTML = `
                <h3>Predicted Digit: ${data.predicted_label} (${data.confidence.toFixed(1)}%)</h3>
                <table class="results-table">
                    <tr>
                        <th>Digit</th>
                        <th>Confidence</th>
                        <th>Probability</th>
                    </tr>
            `;
            
            data.probabilities.forEach((prob, digit) => {
                const width = Math.max(prob, 0.5);
                resultsHTML += `
                    <tr>
                        <td>${digit}</td>
                        <td>${prob.toFixed(1)}%</td>
                        <td>
                            <div class="probability-bar" 
                                    style="width: ${width}%; 
                                        background-color: ${digit === data.predicted_label ? '#4CAF50' : '#ddd'};">
                            </div>
                        </td>
                    </tr>
                `;
            });
            
            resultsHTML += '</table>';
            result.innerHTML = resultsHTML;
        }
    } catch (error) {
        result.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    } finally {
        spinner.style.display = 'none';
    }
});

// Download drawing
downloadBtn.addEventListener('click', () => {
    const link = document.createElement('a');
    link.download = 'digit.png';
    link.href = canvas.toDataURL();
    link.click();
});