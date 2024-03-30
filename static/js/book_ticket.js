function openPdfInNewTab(pdfData) {
    const blob = new Blob([pdfData], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank');
}

document.getElementById('ticket-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const form = this;
    // Send form data via AJAX
    const xhr = new XMLHttpRequest();
    xhr.open(form.method, form.action);
    xhr.responseType = 'arraybuffer';
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Open PDF content in a new tab
            openPdfInNewTab(xhr.response);
        } else {
            console.error('Failed to fetch PDF content');
        }
    };
    xhr.send(new FormData(form));
});