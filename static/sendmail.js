function sendBugReport() {
        fetch('/send_email')
        .then(response => response.text())
        .then(message => alert(message))
        .catch(error => console.error('Error:', error));
    }