// Import necessary functions from the `redis` package
import { createClient, print } from 'redis';

// Create a Redis client instance
const redisClient = createClient();

// Event listener for successful connection to the Redis server
redisClient.on('connect', function() {
  console.log('Redis client connected to the server');
});

// Event listener for errors during the Redis client connection
redisClient.on('error', function(error) {
  console.log(`Redis client not connected to the server: ${error}`);
});

// Set hash key-value pairs in the 'HolbertonSchools' hash
// Each call adds a city and its corresponding value to the hash
redisClient.hset('HolbertonSchools', 'Portland', '50', print);
redisClient.hset('HolbertonSchools', 'Seattle', '80', print);
redisClient.hset('HolbertonSchools', 'New York', '20', print);
redisClient.hset('HolbertonSchools', 'Bogota', '20', print);
redisClient.hset('HolbertonSchools', 'Cali', '40', print);
redisClient.hset('HolbertonSchools', 'Paris', '2', print);

// Retrieve and display all key-value pairs stored in the 'HolbertonSchools' hash
redisClient.hgetall('HolbertonSchools', function(error, result) {
  if (error) {
    console.log(error); // Log any error that occurs during the retrieval
    throw error;        // Rethrow the error to propagate it
  }
  console.log(result);   // Log the retrieved hash object to the console
});
