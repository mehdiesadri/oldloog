// Get the input field
var input = document.getElementById("chat_text");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function(event) {
    var code;

    if (event.key !== undefined) {
        code = event.key;
    } else if (event.keyIdentifier !== undefined) {
        code = event.keyIdentifier;
    } else if (event.keyCode !== undefined) {
        code = event.keyCode;
    }
    // Number 13 is the "Enter" key on the keyboard
    if (code === 13 || code === "Enter") {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        send_message();
    }
});

const endpoint = `/api/chat/v1/session/${roomName}/message/`;

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/' + roomName + "/"
);

chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    let message = data.message;

    if (message) {
        if (message.sender == userID) {
            add_message(message, true);
        } else {
            add_message(message, false);
        }
    } else {
        console.log("message is empty");
    }

    scrollToBottom();
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
    message_attachment = $("#chat_file");
    message_text = message_input.val();
    message_file = message_attachment[0].files[0];
    var formData = new FormData();

    if (message_file) {
        formData.append("attachment", message_file);
        if (!message_text) {
            message_text = message_file.name;
        }
    }
    formData.append("text", message_text);

    $.ajax({
        url: endpoint,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            console.log(data);
            message_input.val("");
            message_attachment.val("");
        },
        error: function(error) {
            console.error(error);
        }
    });
}

function add_message(message, reverse = false) {
    let chat_content = document.getElementById("chat-content");
    let class_name = "media media-chat";
    let avatar = `<img class="avatar" src="${message.avatar}" alt="user-avatar">`;
    let attachment = "";

    if (reverse) {
        class_name += " media-chat-reverse";
        avatar = "";
    }

    if (message.attachment) {
        attachment = `<p style="background-color: transparent; font-size: small;">` +
            `<a style="text-decoration: inherit; color: black;" target="blank" href="${message.attachment}">` +
            `Download attachment` +
            `</a>` +
            `</p>`;
    }

    let datetime = new Date(message.created_at);
    datetime = datetime.toLocaleString("en-US");

    chat_content.innerHTML += `<div class="${class_name}">` +
        avatar +
        `<div class="media-body">
            <p>${message.text}</p>` +
        attachment +
        `<p class="meta">${datetime}</p>
        </div>
    </div>`;
}

function fetch_messages(roomName) {
    $.ajax({
        url: endpoint + '?limit=1000',
        method: "GET",
        success: function(data) {
            data.results.reverse().forEach(message => {
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

fetch_messages(roomName);