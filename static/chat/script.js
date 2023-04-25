const message = document.getElementById('message');
const chat = document.getElementById('chat');
const refresh = document.getElementById('refresh');
const send = document.getElementById('send');
let response;

function userMessage(message) {
    chat.innerHTML += `
        <div class='user'>
            ` + message + `
        </div>
    `;
}

function aiMessage(message) {
    chat.innerHTML += `
        <div class='ai'>
            ` + message + `
        </div>
    `;
}

refresh.onclick = () => {
    server.refresh();
    location.reload();
}

send.onclick = () => {
    text();
}

function text() {
    userMessage(message.value);
    server.text(message.value);
    message.value = '';
}

message.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        text();
    }
});

window.onload = () => {
    server.refresh();
}