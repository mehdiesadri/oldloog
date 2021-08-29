$('document').ready(function() {
    // Document is ready.
    console.log("Seyyed Ali Ayati");
    $(".alert-error").toggleClass('alert-error', 'alert-danger');

    // Setup AJAX
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

});

const notificationSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/'
);

notificationSocket.onopen = function(e) {
    console.log("Opened...");
}

notificationSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    let message = data.message;

    if (message) {
        console.log(message);
    } else {
        console.log("message is empty");
    }
}

notificationSocket.onclose = function(e) {
    console.log("The socket closed....");
    console.log(e);
}