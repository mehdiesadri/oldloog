let chatSocket;

function send_message() {
    message_input = $("#chat_text");
    message_text = message_input.val();
    message_input.val("");
}

function set_session(roomName) {
    chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/' + roomName + "/"
    );

    chatSocket.onmessage = function(e) {
        console.log("onMessage");
        let data = JSON.parse(e.data);

        if (data.message) {
            console.log(data);
        } else {
            console.log("message is empty");
        }
    }

    chatSocket.onclose = function(e) {
        console.log("The socket closed....");
    }
}