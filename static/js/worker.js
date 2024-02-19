// worker.js

// Event listener for messages from the main thread
self.addEventListener('message', function(e) {
    var direction = e.data.direction;

    // Perform the corresponding action based on the direction received
    switch (direction) {
        case 'left':
            moveleft();
            break;
        case 'right':
            moveRight();
            break;
        default:
            // No action for other directions
            break;
    }
}, false);

// Function to move the servo left
function moveleft() {
    // Send POST request to move_servo_channel2 endpoint with direction 'left'
    sendPostRequest('/move_servo_channel2', { direction: 'left', step: 5 });
}

// Function to move the servo right
function moveRight() {
    // Send POST request to move_servo_channel2 endpoint with direction 'right'
    sendPostRequest('/move_servo_channel2', { direction: 'right', step: 5 });
}

// Function to send a POST request
function sendPostRequest(url, data) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Response:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
