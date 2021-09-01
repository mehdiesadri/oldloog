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

    switch (message) {
        case 'redirect':
            if (window.location.href !== data.data.url) {
                window.location.href = data.data.url;
            }
            break;

        default:
            console.log(message);
            break;
    }
}

notificationSocket.onclose = function(e) {
    console.log("The socket closed....");
    console.log(e);
}