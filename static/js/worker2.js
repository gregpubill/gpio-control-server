// worker.js

// Event listener for messages from the main thread
self.addEventListener('message', function(e) {
    var direction = e.data.direction;

    // Perform the corresponding action based on the direction received
    switch (direction) {
        case 'up':
            moveForward();
            break;
        case 'down':
            moveReverse();
            break;
        default:
            // No action for other directions
            break;
    }
}, false);

// Function 
function moveForward() {
    // Send POST request to /forward_slow endpoint with direction 'up'
    sendPostRequest('/forward_slow', {direction: 'up'});
}

// Function to move the servo right
function moveReverse() {
    // Send POST request to  endpoint with direction 
    sendPostRequest('/move_reverse', {direction: 'down'});
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
