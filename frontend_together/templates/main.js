
window.addEventListener("DOMContentLoaded", () => {
  const chat = document.querySelector(".chat-form");
  // Open the WebSocket connection and register event handlers.

  var path = location.pathname.split('/');
  if (path[path.length-1].indexOf('.html')>-1) {
    path.length = path.length - 1;
  }
  var roomPath = path.join('/'); //  if you want the whole thing like '/one/two/three'
  console.log(roomPath);


  const websocket = new WebSocket("ws://localhost:8001"+ roomPath +"?token=123");

  const xz = JSON.stringify({message: "event"})
  websocket.onopen = () => websocket.send(xz);
  receiveMoves(chat, websocket);
  sendMoves(chat, websocket);
});


function sendMoves(chat, websocket) {
  chat.addEventListener("submit", function(e) {
    e.preventDefault()
    const messageelement = document.getElementById('chat-text');
    const message = messageelement.value;

    if (message === '') {
      return;
    }
    const event = {
      event_type: "chat_message",
      user_id: "user_1",
      message: message,
    };
    websocket.send(JSON.stringify(event));
    console.log(message);
    messageelement.value = "";
  });
}

function receiveMoves(board, websocket) {
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    console.log(data)
    switch (event.event_type) {
      case "chat_message":
        // Update the UI with the move.
        chatAdd(event.message, event.from);
        break;
      case "player_command":
        // ...
        break;
      case "error":
        // ...
        break;
      default:
        throw new Error("Unsupported event type: ${event.type}.");
    }
  });
}


function chatAdd(message, user) {
  const board = document.getElementById('board');
  board.innerHTML += '<p>' + user + ': ' + message + '</p>';
}