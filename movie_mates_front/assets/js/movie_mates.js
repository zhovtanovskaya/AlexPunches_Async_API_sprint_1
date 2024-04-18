document.documentElement.setAttribute('data-bs-theme', 'dark');
const myModal = new bootstrap.Modal(document.getElementById('myModal'));
myModal.show();
const myModalEl = document.getElementById('myModal');
let controls = ['mute', 'volume', 'fullscreen', 'current-time'];
let clickToPlay = true;
let playerHtmlvideo = new Plyr('video', {
    controls: controls,
    clickToPlay: clickToPlay,
    player_type: 'lead',
});
playerHtmlvideo.player_type = 'watcher';


window.addEventListener("DOMContentLoaded", () => {
    const chat = document.querySelector(".chat-form");
    const websocket = new WebSocket("ws://localhost:8001/{{ room_id }}?token={{ token }}");

    receiveMoves(chat, websocket);
    sendMoves(chat, websocket);
});



function sendMoves(chat, websocket) {
    chat.addEventListener("submit", function(e) {
        e.preventDefault()
        const messageelement = document.getElementById('chat-text');
        const messageText = messageelement.value;

        if (messageText === '') {
            return;
        }
        const messageObj = {
            event_type: "broadcast_message",
            payload: {
                "message": messageText,
            },
        };
        websocket.send(JSON.stringify(messageObj));
        messageelement.value = "";
    });

    // Когда закрываем приветственное модальное окно, запрашиваем стейт плеера, чтобы переключить на нужное время
    myModalEl.addEventListener('hide.bs.modal', function (event) {
        const messageObj = {
            event_type: "room_request",
            payload: {
                "command": "get_player_state",
            },
        };
        websocket.send(JSON.stringify(messageObj));
    });
}

function receiveMoves(board, websocket) {
    websocket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data);
        const payload = event.payload;
        switch (event.event_type) {
            case "broadcast_message":
                chatAdd(payload.message, payload.from_user);
                break;
            case "player_state":
                if (payload.player_type === 'lead' && playerHtmlvideo.player_type !== 'lead'){
                    playerInit('lead', websocket);
                }
                if (payload.timecode) {
                    playerHtmlvideo.currentTime = payload.timecode;
                }
                if (payload.player_status === 'play'){
                    playerHtmlvideo.play();
                }
                if (payload.player_status === 'pause'){
                    playerHtmlvideo.pause();
                }
                break;
            case "chat_state":
                const chatMessages = payload.chat_messages;
                chatMessages.forEach((item, index, array) => {
                    chatAdd(item.message, item.user_name);
                })
                break;
            case "broadcast_command":
                if (payload.timecode) {
                    playerHtmlvideo.currentTime = payload.timecode;
                }
                if (payload.player_status === 'play'){
                    playerHtmlvideo.play();
                }
                if (payload.player_status === 'pause'){
                    playerHtmlvideo.pause();
                }
                break;
            case "video_state":
                break;
            case "error":
                const errorMessages = payload.message;
                console.log(errorMessages)
                break;
            default:
                console.log(event.event_type)
                throw new Error("Unsupported event type: ${event.type}.");
        }
    });
}

function playerInit(type, websocket) {
    if (type === 'lead') {
        playerHtmlvideo.destroy()
        controls = ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'airplay', 'fullscreen'];
        clickToPlay = true;
        playerHtmlvideo = new Plyr('video', {
            controls: controls,
            clickToPlay: clickToPlay,
        });
        playerHtmlvideo.player_type = 'lead';

        playerHtmlvideo.on('play', (event) => {
            const messageObj = {
                event_type: "broadcast_command",
                payload: {
                    'timecode': playerHtmlvideo.currentTime,
                    'player_status': 'play',
                },
            };
            websocket.send(JSON.stringify(messageObj));
        });
        playerHtmlvideo.on('pause', (event) => {
            const messageObj = {
                event_type: "broadcast_command",
                payload: {
                    'timecode': playerHtmlvideo.currentTime,
                    'player_status': 'pause',
                },
            };
            websocket.send(JSON.stringify(messageObj));
        });
        playerHtmlvideo.on('seeked', (event) => {
            const messageObj = {
                event_type: "broadcast_command",
                payload: {
                    'timecode': playerHtmlvideo.currentTime,
                },
            };
            websocket.send(JSON.stringify(messageObj));
            console.log('seeked')

            setInterval(setState, 3000, websocket)



        });
    }

}

function setState(websocket){
    let player_status = 'stop'
    if (playerHtmlvideo.playing) {
        player_status = 'play'
    } else if (playerHtmlvideo.paused) {
        player_status = 'pause'
    }

    const stateObj = {
        event_type: "room_request",
        payload: {
            'timecode': playerHtmlvideo.currentTime,
            'player_status': player_status,
            'speed': playerHtmlvideo.speed,
            'command': 'set_state',
        },
    };
    websocket.send(JSON.stringify(stateObj));
}


function chatAdd(message, user) {
    const board = document.getElementById('board');
    board.innerHTML += '<p>' + user + ': ' + message + '</p>';
}