window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:8765/test_room/");
    websocket.onmessage = (event) => {
        console.log("Server response:", event.data);
    };
    websocket.onclose = (event) => {
        console.log("Connection closed");
    };
    const chat = document.querySelector(".chat-form");
    sendMoves(chat, websocket);
});


function addChatMessage(message, author) {
    const board = document.getElementById('board');
    board.innerHTML += '<p>' + author + ': ' + message + '</p>';
}


function getChatMessage() {
    const messageelement = document.getElementById('chat-text');
    const messageText = messageelement.value;
    messageelement.value = "";
    return messageText;
}


function sendMoves(chat, websocket) {
    chat.addEventListener("submit", function(e) {
        e.preventDefault()
        const messageText = getChatMessage()
        if (messageText === '') {
            return;
        }
        const messageObj = {
            type: "send_text",
            to: "__all__",
            text: messageText,
        };
        websocket.send(JSON.stringify(messageObj));
    });
}