const ws = new WebSocket('ws://localhost:8765');

ws.onopen = () => {
    document.getElementById('status').innerText = 'Connected to server';
};

ws.onmessage = event => {
    document.getElementById('status').innerText = event.data;
};

ws.onerror = error => {
    console.error('WebSocket Error:', error);
    document.getElementById('status').innerText = 'Error connecting to server';
};

ws.onclose = () => {
    document.getElementById('status').innerText = 'Disconnected from server';
};

document.getElementById('schedule-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const lightOn = document.getElementById('on-time').value;
    const lightOff = document.getElementById('off-time').value;
    if (!lightOn || !lightOff) {
        alert('Please enter both ON and OFF times');
        return;
    }
    const timings = { onTime: lightOn, offTime: lightOff };
    try {
        ws.send(JSON.stringify(timings));
        console.log('Sent schedule:', timings);
    } catch (err) {
        console.error('Send error:', err);
        document.getElementById('status').innerText = 'Failed to send schedule';
    }
});
