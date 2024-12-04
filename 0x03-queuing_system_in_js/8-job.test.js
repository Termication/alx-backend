// Import necessary testing functions and libraries
import { describe, it, before, after, afterEach } from 'mocha'; // Mocha framework for structuring tests
import { expect } from 'chai'; // Chai library for assertions
import { createQueue } from 'kue'; // Kue for managing job queues

// Import the function to test
import createPushNotificationsJobs from './8-job.js';

// Create a Kue queue instance
const queue = createQueue();

// Group tests for the `createPushNotificationsJobs` function
describe('Test createPushNotificationsJobs function', function() {
  // Hook to run before all tests: enters test mode for the queue
  before(function () {
    queue.testMode.enter();
  });

  // Hook to run after each test: clears all jobs in test mode
  afterEach(function () {
    queue.testMode.clear();
  });

  // Hook to run after all tests: exits test mode for the queue
  after(function () {
    queue.testMode.exit();
  });

  // Test case to check if an error is thrown when input is not an array
  it('display an error message if jobs is not an array', function() {
    // Expect the function to throw an error with a specific message
    expect(() => createPushNotificationsJobs('job', queue)).to.throw(Error, 'Jobs is not an array');
  });

  // Test case to validate if jobs are correctly created in the queue
  it('Test whether jobs are created', function() {
    // Define a list of jobs with phone numbers and messages
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      },
    ];

    // Call the function to add jobs to the queue
    createPushNotificationsJobs(jobs, queue);

    // Assert that the correct number of jobs are added to the queue
    expect(queue.testMode.jobs.length).to.equal(2);

    // Validate the type and data of the first job
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.eql(jobs[0]);

    // Validate the type and data of the second job
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].data).to.eql(jobs[1]);
  });
});
