var wsProtocol = "wss://";

if (location.protocol !== 'https:') {
    wsProtocol = "ws://";
}

const AUDIO = new Audio("https://assets.mixkit.co/sfx/preview/mixkit-positive-notification-951.mp3");
AUDIO.load();

const notificationSocket = new WebSocket(
    wsProtocol + window.location.host + '/ws/notifications/'
);

// Initialize Firebase
const firebaseConfig = {
    apiKey: "AIzaSyDGRGwxGQ5irefOaJyYX3Neoh7NU8O1M2Q",
    authDomain: "loog-test-notification.firebaseapp.com",
    projectId: "loog-test-notification",
    storageBucket: "loog-test-notification.appspot.com",
    messagingSenderId: "504975596104",
    appId: "1:504975596104:web:ef4559f61eb8db3437167d",
    measurementId: "G-YTSSV408R3"
};

firebase.initializeApp(firebaseConfig);
console.log("Firebase Initialized...");

// Firebase Messaging Service
const messaging = firebase.messaging();

notificationSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);

    switch (data.type) {
        case 'system_message':
            if (data.title === "REDIRECT") {
                if (window.location.href !== data.url) {
                    window.location.href = data.url;
                }
            } else if (data.title === "NEW_LOOG") {
                // Play and show popup
                new Audio("https://assets.mixkit.co/sfx/preview/mixkit-positive-notification-951.mp3").play();

                Swal.fire({
                    titleText: 'New loog is available!',
                    text: data.body,
                    imageUrl: data.icon_url,
                    imageAlt: 'user-profile',
                    showDenyButton: true,
                    confirmButtonText: 'Accept',
                    denyButtonText: 'Reject',
                }).then((result) => {
                    /* Read more about isConfirmed, isDenied below */
                    if (result.isConfirmed) {
                        window.location.href = data.url;
                    }
                })
            }
            break;

        case 'notification_message':
            add_notification(data);
            break;

        default:
            console.log(data);
            break;
    }
}

notificationSocket.onclose = function (e) {
    console.log(e);
}

function notification_click(id, url) {
    $.ajax({
        url: `/api/notifications/v1/notifications/${id}/`,
        method: 'PATCH',
        data: { 'read': true },
        success: function (data) {
            if (url !== 'null')
                window.location.href = url;
            else {
                $("#notification_" + id).remove();
            }
        },
        error: function (error) {
            console.error(error);
        }
    });
}


function add_notification(notification) {
    $("#notificationList").prepend(`<a id="notification_${notification.id}" onclick="notification_click(${notification.id}, '${notification.url}');" class="list-group-item list-group-item-action">
                                    <div class="row align-items-center">
                                        <div class="col-auto">
                                            <!-- Avatar -->
                                            <img alt="Image placeholder" src="${notification.icon_url || '/static/img/brand/loog.png'}"
                                                 class="avatar rounded-circle">
                                        </div>
                                        <div class="col ml--2">
                                            <div class="d-flex justify-content-between align-items-center">
                                                <div>
                                                    <h4 class="mb-0 text-sm">${notification.title}</h4>
                                                </div>
                                                <div class="text-right text-muted">
                                                    <small>${new Date(notification.created_at).toLocaleString("en-US")}</small>
                                                </div>
                                            </div>
                                            <p class="text-sm mb-0">${notification.body}</p>
                                        </div>
                                    </div>
                                </a>`);
}

function wait_list_click() {
    Swal.fire({
        title: 'Enter your email address:',
        input: 'text',
        inputAttributes: {
            autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: 'Join!',
        showLoaderOnConfirm: true,
        preConfirm: (email) => {
            return fetch(`/api/accounts/v1/waitlist/?email=${email}`)
                .then(response => {
                    if (!response.ok) {
                        console.log(response)
                        throw new Error(response.statusText)
                    }
                    return response.json()
                })
                .catch(error => {
                    Swal.showValidationMessage(
                        `Request failed: ${error}`
                    )
                })
        },
        allowOutsideClick: () => !Swal.isLoading()
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: `Check your mailbox!`,
            })
        }
    });
}

function sendTokenToServer(currentToken) {
    console.log("Token ", currentToken);

    if (!isTokenSentToServer()) {
        $.ajax({
            url: "/api/notifications/v1/devices/",
            method: "POST",
            async: false,
            data: {
                'registration_id': currentToken,
                'type': 'web'
            },
            success: function (data) {
                console.log(data);
                setTokenSentToServer(true);
            },
            error: function (err) {
                console.log(err);
                setTokenSentToServer(false);
            }
        });

    } else {
        console.log('Token already sent to server so won\'t send it again ' +
            'unless it changes');
    }
}

function isTokenSentToServer() {
    return window.localStorage.getItem("sentToServer") === "1";
}

function setTokenSentToServer(sent) {
    if (sent) {
        window.localStorage.setItem("sentToServer", "1");
    } else {
        window.localStorage.setItem("sentToServer", "0");
    }
}


function requestPermission() {
    messaging.requestPermission().then(function () {
        console.log("Has permission!");
        resetUI();
    }).catch(function (err) {
        console.log('Unable to get permission to notify.', err);
    });
}

function resetUI() {
    console.log("In reset ui");
    messaging.getToken().then(function (currentToken) {
        console.log(currentToken);
        if (currentToken) {
            sendTokenToServer(currentToken);
        } else {
            setTokenSentToServer(false);
        }
    }).catch(function (err) {
        console.log(err);
        setTokenSentToServer(false);
    });
}


$('document').ready(function () {
    // Document is ready.

    // Setup AJAX
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
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

    // Get Notifications
    $.ajax({
        url: '/api/notifications/v1/notifications/',
        method: 'GET',
        success: function (data) {
            $("#notificationCount").text(data.length);
            data.forEach(notification => {
                add_notification(notification);
            });
        },
        error: function (error) {
            console.error(error);
        }
    });

    messaging.onTokenRefresh(function () {
        messaging.getToken().then(function (refreshedToken) {
            console.log("Token refreshed.");
            // Indicate that the new Instance ID token has not yet been sent to the
            // app server.
            setTokenSentToServer(false);
            // Send Instance ID token to app server.
            sendTokenToServer(refreshedToken);
            resetUI();
        }).catch(function (err) {
            console.log("Unable to retrieve refreshed token ", err);
        });
    });

    messaging.onMessage(function (payload) {
        payload = payload.data;
        console.log("Message received. ", payload);

        const notificationTitle = payload.title;
        const notificationOptions = {
            body: payload.body,
            icon: payload.icon_url,
        };

        if (!("Notification" in window)) {
            console.log("This browser does not support system notifications");
        }
        // Let's check whether notification permissions have already been granted
        else if (Notification.permission === "granted") {
            // If it's okay let's create a notification
            var notification = new Notification(notificationTitle, notificationOptions);
            notification.onclick = function (event) {
                event.preventDefault(); // prevent the browser from focusing the Notification's tab
                window.open(payload.url, '_blank');
                notification.close();
            }
        }
    });


    requestPermission();



});