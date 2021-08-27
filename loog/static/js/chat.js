const endpoint = `/api/chat/v1/session/${roomName}/message/`;

const chatSocket = new WebSocket(
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

function scrollToBottom() {
    let objDiv = document.getElementById("chat-content");
    objDiv.scrollTop = objDiv.scrollHeight;
}

function send_message() {
    message_input = $("#chat_text");
    message_text = message_input.val();
    message_input.val("");
}

function add_message(message, reverse = false) {
    let chat_content = document.getElementById("chat-content");
    let class_name = "media media-chat";
    let avatar = `<img class="avatar" src="${message.avatar}" alt="user-avatar">`;

    if (reverse) {
        class_name += " media-chat-reverse";
        avatar = "";
    }

    let datetime = new Date(message.created_at);
    datetime = datetime.toLocaleString("en-US");

    chat_content.innerHTML += `<div class="${class_name}">` +
        avatar +
        `<div class="media-body">
            <p>${message.text}</p>
            <p class="meta">${datetime}</p>
        </div>
    </div>`;
}

function fetch_messages(roomName) {
    $.ajax({
        url: endpoint,
        method: "GET",
        success: function(data) {
            data.results.forEach(message => {
                console.log(message);
                if (message.sender == userID) {
                    add_message(message, true);
                } else {
                    add_message(message, false);
                }
            });

            scrollToBottom();
        },
        error: function(error) {
            console.error(error);
        }
    });
    console.log(roomName);
}

fetch_messages(roomName);