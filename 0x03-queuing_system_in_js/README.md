# Redis and Node.js Guide

This repository provides a comprehensive guide for working with Redis and Node.js, covering everything from setting up a Redis server to building a basic Express app that interacts with Redis and a queue system.
Table of Contents

    Prerequisites
    How to Run a Redis Server
    Simple Operations with the Redis Client
    Using Redis with Node.js
    Storing Hash Values in Redis
    Dealing with Async Operations in Redis
    Using Kue as a Queue System
    Building an Express App with Redis
    Building an Express App with Redis and Kue

# Prerequisites

    Redis: Installed on your machine. You can install Redis by following the official Redis documentation.
    Node.js: Ensure you have Node.js installed. Download it from the Node.js website.
    npm: Included with Node.js for package management.

# How to Run a Redis Server

    Install Redis on your system if not already installed.
    Start the Redis server by running:

redis-server

Confirm the server is running by connecting with the Redis client:

    redis-cli ping

    The response should be PONG.

Simple Operations with the Redis Client

    Open the Redis CLI:

redis-cli

Perform basic operations:

    Set a value:

SET key value

Get a value:

GET key

Delete a key:

        DEL key

Using Redis with Node.js

    Install the Redis package for Node.js:

npm install redis

Connect to Redis in your Node.js application:

const redis = require('redis');
const client = redis.createClient();

client.on('connect', () => {
    console.log('Connected to Redis!');
});

client.on('error', (err) => {
    console.error('Redis error:', err);
});

Perform basic operations:

    client.set('key', 'value', redis.print);
    client.get('key', (err, reply) => {
        if (err) throw err;
        console.log(reply);
    });

Storing Hash Values in Redis

    Use the hmset command to store hash values:

client.hmset('user:1000', 'name', 'John', 'age', '30', 'country', 'USA');

Retrieve hash values:

    client.hgetall('user:1000', (err, object) => {
        if (err) throw err;
        console.log(object);
    });

Dealing with Async Operations in Redis

    Use Promises with a library like util.promisify:

    const { promisify } = require('util');
    const getAsync = promisify(client.get).bind(client);

    async function fetchValue(key) {
        const value = await getAsync(key);
        console.log(value);
    }
    fetchValue('key');

Using Kue as a Queue System

    Install Kue:

npm install kue

Create a queue and add jobs:

const kue = require('kue');
const queue = kue.createQueue();

const job = queue.create('email', {  
    title: 'Welcome Email',  
    to: 'user@example.com',  
    template: 'welcome'  
}).save((err) => {
    if (!err) console.log(job.id);
});

Process jobs:

    queue.process('email', (job, done) => {
        console.log(`Processing job ${job.id}`);
        done();
    });

Building an Express App with Redis

    Install Express and Redis:

npm install express redis

Set up the Express app:

    const express = require('express');
    const redis = require('redis');

    const app = express();
    const client = redis.createClient();

    app.get('/data', (req, res) => {
        client.get('key', (err, reply) => {
            if (err) res.status(500).send(err);
            res.send(reply);
        });
    });

    app.listen(3000, () => {
        console.log('Server running on port 3000');
    });

Building an Express App with Redis and Kue

    Integrate Kue into your Express app:

    const kue = require('kue');
    const queue = kue.createQueue();

    app.post('/job', (req, res) => {
        const job = queue.create('jobType', { data: 'example' }).save();
        res.send(`Job created: ${job.id}`);
    });

    queue.process('jobType', (job, done) => {
        console.log(`Processing job ${job.id}`);
        done();
    });

    Run the app and process jobs simultaneously.

Conclusion

This guide equips you with the knowledge to:

    Use Redis for caching and storage.
    Build applications with Redis and Node.js.
    Leverage Kue for queue management in your apps.
