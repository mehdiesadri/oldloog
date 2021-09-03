// Register event listener for the 'push' event.
self.addEventListener('push', function(event) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
    // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const title = data.title || 'New Notification 🕺🕺';
    const body = data.body || 'This is default content. Your notification didn\'t have one 🙄🙄';
    const icon_url = data.icon_url || 'https://i.imgur.com/MZM3K5w.png';
    const url = data.url || 'https://www.google.com/';

    // Keep the service worker alive until the notification is created.
    event.waitUntil(
        self.registration.showNotification(title, {
            body: body,
            icon: icon_url,
            data: {
                url: url,
            }
        })
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(
        clients.openWindow(event.notification.data.url)
    );
});