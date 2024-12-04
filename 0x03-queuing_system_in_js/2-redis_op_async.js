// Import the `createClient` function and `print` utility from the `redis` package
import { createClient, print } from 'redis';
// Import the `promisify` function from the `util` package to handle asynchronous operations more cleanly
import { promisify } from 'util';

// Create a Redis client instance
const client = createClient();

// Set up an event listener for when the client successfully connects to the Redis server
client.on('connect', function() {
  console.log('Redis client connected to the server');
});

// Set up an event listener for when there is an error with the Redis client
client.on('error', function (err) {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Function to set a new key-value pair in the Redis store
function setNewSchool(schoolName, value) {
  // Use the `set` method to store the key-value pair and log the result using the `print` utility
  client.set(schoolName, value, print);
};

// Promisify the `get` method to use async/await syntax for fetching values
const get = promisify(client.get).bind(client);

// Asynchronous function to fetch and display the value of a given key
async function displaySchoolValue(schoolName) {
  // Use the promisified `get` function to retrieve the value
  const result = await get(schoolName).catch((error) => {
    // Handle errors if the `get` operation fails
    if (error) {
      console.log(error);
      throw error; // Rethrow the error to propagate it
    }
  });
  // Log the fetched value to the console
  console.log(result);
}

// Fetch and display the value of the key 'Holberton' (key may not exist initially)
displaySchoolValue('Holberton');

// Set a new key-value pair: 'HolbertonSanFrancisco' => '100'
setNewSchool('HolbertonSanFrancisco', '100');

// Fetch and display the value of the newly set key 'HolbertonSanFrancisco'
displaySchoolValue('HolbertonSanFrancisco');

