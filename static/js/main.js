const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const fileInfo = document.getElementById('fileInfo');
const processBtn = document.getElementById('processBtn');
const clearUploadBtn = document.getElementById('clearUploadBtn');
const resultsText = document.getElementById('resultsText');
const wordCount = document.getElementById('wordCount');
const charCount = document.getElementById('charCount');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const clearTextBtn = document.getElementById('clearTextBtn');
const shareBtn = document.getElementById('shareBtn');

let selectedFile = null;

uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFile(e.dataTransfer.files[0]);
});

fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

processBtn.addEventListener('click', () => {
    if (!selectedFile) return;
    processBtn.disabled = true;
    processBtn.textContent = 'Processing...';
    uploadFile(selectedFile)
        .finally(() => {
            processBtn.disabled = false;
            processBtn.textContent = '✨ Process Image';
        });
});

clearUploadBtn.addEventListener('click', () => {
    resetUploadState();
    resetResults();
});

copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(resultsText.value || '').then(() => {
        const original = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied!';
        setTimeout(() => { copyBtn.textContent = original; }, 1500);
    });
});

downloadBtn.addEventListener('click', () => {
    if (!resultsText.value) return;
    const blob = new Blob([resultsText.value], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'extracted_text.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

clearTextBtn.addEventListener('click', () => {
    resetResults();
});

shareBtn.addEventListener('click', () => {
    if (!navigator.share) return alert('Share not supported on this browser');
    navigator.share({ title: 'Extracted Text', text: resultsText.value || '' });
});

resultsText.addEventListener('input', updateStats);

document.addEventListener('dragover', (e) => e.preventDefault());
document.addEventListener('drop', (e) => e.preventDefault());

function handleFile(file) {
    if (!file) return;

    const maxSize = 16 * 1024 * 1024;
    const isPdf = file.type === 'application/pdf';
    const isImage = file.type.startsWith('image/');

    if (!isPdf && !isImage) {
        alert('Please upload an image or PDF');
        return;
    }

    if (file.size > maxSize) {
        alert('File must be under 16MB');
        return;
    }

    selectedFile = file;
    processBtn.disabled = false;

    if (isImage) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.src = e.target.result;
            preview.classList.add('show');
        };
        reader.readAsDataURL(file);
    } else {
        preview.classList.remove('show');
        preview.removeAttribute('src');
    }

    fileInfo.textContent = `📁 ${file.name} • ${(file.size / 1024).toFixed(1)} KB`;
    fileInfo.classList.add('show');
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    return fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.error) throw new Error(data.error);
            resultsText.value = data.text || '';
            updateStats(data);
            enableResultButtons();
        })
        .catch((err) => {
            alert(err.message || 'Error processing file');
            resetResults();
        });
}

function updateStats(data) {
    const text = resultsText.value;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const chars = text.length;
    wordCount.textContent = data?.word_count ?? words;
    charCount.textContent = data?.char_count ?? chars;
}

function enableResultButtons() {
    const hasText = Boolean(resultsText.value);
    copyBtn.disabled = !hasText;
    downloadBtn.disabled = !hasText;
    clearTextBtn.disabled = !hasText;
    shareBtn.disabled = !hasText;
}

function resetResults() {
    resultsText.value = '';
    wordCount.textContent = '0';
    charCount.textContent = '0';
    copyBtn.disabled = true;
    downloadBtn.disabled = true;
    clearTextBtn.disabled = true;
    shareBtn.disabled = true;
}

function resetUploadState() {
    selectedFile = null;
    fileInput.value = '';
    preview.classList.remove('show');
    preview.removeAttribute('src');
    fileInfo.classList.remove('show');
    processBtn.disabled = true;
}
