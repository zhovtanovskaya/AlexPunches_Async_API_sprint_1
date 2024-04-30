window.addEventListener("DOMContentLoaded", () => {
    let playerHtmlVideo = new Plyr('video', {
        controls: ['mute', 'volume', 'fullscreen', 'current-time'],
        clickToPlay: false,
    });
    let isLeading = false;
    const websocket = new WebSocket("ws://localhost:8765/test_room/");
    websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Server response:', data);
        if (data.type === 'incoming_text') {
            addChatMessage(data.text, data.author);
        }
        if (data.type === 'set_leading_client') {
            isLeading = true;
            setLeadingPlayer(playerHtmlVideo, websocket)
        }
        if (data.type === 'leading_player_changed') {
            if (isLeading === false) {
                playerHtmlVideo.currentTime = data.timecode;
                if (data.player_status === 'play'){
                    playerHtmlVideo.play();
                }
                if (data.player_status === 'pause'){
                    playerHtmlVideo.pause();
                }
            }
        }
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
    messageelement.value = '';
    return messageText;
}


function setLeadingPlayer(player, websocket) {
    // Разрешить элементы управления воспроизведением.
    player.destroy();
    controls = ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'airplay', 'fullscreen'];
    player = new Plyr('video', {
        controls: controls,
        clickToPlay: true,
    });
    player.on('play', (event) => {
        const messageObj = {
            type: 'leading_player_changed',
            'timecode': player.currentTime,
            'player_status': 'play',
        };
        json = JSON.stringify(messageObj);
        websocket.send(json);
    });
    player.on('pause', (event) => {
        const messageObj = {
            type: 'leading_player_changed',
            'timecode': player.currentTime,
            'player_status': 'pause',
        };
        json = JSON.stringify(messageObj);
        websocket.send(json);
    });
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