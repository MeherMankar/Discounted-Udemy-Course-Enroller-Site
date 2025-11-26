// Keep Render service alive (prevents sleep after 15min)
setInterval(() => {
    fetch('/keepalive')
        .then(response => response.json())
        .then(data => console.log('Keepalive:', data.timestamp))
        .catch(err => console.log('Keepalive failed:', err));
}, 14 * 60 * 1000); // Every 14 minutes