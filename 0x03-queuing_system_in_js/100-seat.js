import { createClient } from 'redis';
import { createQueue } from 'kue';
import { promisify } from 'util';
import express from 'express';

// Initialize Redis client
const redisClient = createClient();

// Event listener for successful Redis connection
redisClient.on('connect', function() {
  console.log('Redis client connected to the server');
});

// Event listener for Redis connection error
redisClient.on('error', function(err) {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Promisify Redis `get` function to allow async/await usage
const asyncGet = promisify(redisClient.get).bind(redisClient);

/**
 * Sets the number of available seats in Redis.
 * @param {number} number - The number of available seats to reserve.
 */
function reserveSeat(number) {
  redisClient.set('available_seats', number);
}

/**
 * Retrieves the current number of available seats from Redis.
 * @returns {Promise<number>} - The number of available seats.
 */
async function getCurrentAvailableSeats() {
  const seats = await asyncGet('available_seats');
  return seats;
}

// Flag to enable or disable reservations
let reservationEnabled = true;

// Create a Kue queue for job processing
const queue = createQueue();

// Initialize Express application
const app = express();

/**
 * Endpoint to retrieve the current number of available seats.
 * Responds with a JSON object containing the number of seats.
 */
app.get('/available_seats', async function(req, res) {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ "numberOfAvailableSeats": availableSeats });
});

/**
 * Endpoint to create a seat reservation job.
 * If reservations are disabled, responds with a blocked status.
 * Otherwise, adds a job to the queue and responds with the status.
 */
app.get('/reserve_seat', function(req, res) {
  if (!reservationEnabled) {
    res.json({ "status": "Reservations are blocked" });
    return;
  }

  const job = queue.create('reserve_seat', { 'seat': 1 }).save((error) => {
    if (error) {
      res.json({ "status": "Reservation failed" });
      return;
    } else {
      res.json({ "status": "Reservation in process" });

      // Log job completion
      job.on('complete', function() {
        console.log(`Seat reservation job ${job.id} completed`);
      });

      // Log job failure
      job.on('failed', function(error) {
        console.log(`Seat reservation job ${job.id} failed: ${error}`);
      });
    }
  });
});

/**
 * Endpoint to start processing the queue.
 * Processes `reserve_seat` jobs and updates available seats in Redis.
 * If no seats are available, disables further reservations.
 */
app.get('/process', function(req, res) {
  res.json({ "status": "Queue processing" });

  queue.process('reserve_seat', async function(job, done) {
    const seat = Number(await getCurrentAvailableSeats());

    if (seat === 0) {
      reservationEnabled = false;
      done(Error('Not enough seats available'));
    } else {
      reserveSeat(seat - 1);
      done();
    }
  });
});

// Start the Express server on the specified port
const port = 1245;
app.listen(port, () => {
  console.log(`App is listening at http://localhost:${port}`);
});

// Initialize available seats in Redis
reserveSeat(50);
