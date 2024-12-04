// Import the `createClient` function from the `redis` package
import { createClient } from 'redis';

// Create a Redis client instance for publishing messages
const publisher = createClient();

// Event listener for successful connection to the Redis server
publisher.on('connect', function () {
    console.log('Redis client connected to the server');
});

// Event listener for errors during connection to the Redis server
publisher.on('error', function(error) {
    console.log(`Redis client not connected to the server: ${error.message}`);
});

// Function to publish a message to the 'holberton school channel'
/**
 * Publishes a message to the Redis channel after a delay.
 * @param {string} message - The message to be published.
 * @param {number} time - The delay in milliseconds before sending the message.
 */
function publishMessage(message, time) {
  setTimeout(function () {
    console.log(`About to send: ${message}`);
    publisher.publish('holberton school channel', message);
  }, time);
}

// Publish several messages with varying delays
publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300); // Special message to trigger server shutdown
publishMessage("Holberton Student #3 starts course", 400);
