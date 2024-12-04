import { createClient } from 'redis';
import express from 'express';
import { promisify } from 'util';

// Create an Express application and set it to run on port 1245
const app = express();

// Initialize a Redis client
const redisClient = createClient();

// Log connection success to Redis server
redisClient.on('connect', function() {
  console.log('Redis client connected to the server');
});

// Log connection errors to Redis server
redisClient.on('error', function(err) {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Promisify the Redis `get` function for async/await usage
const get = promisify(redisClient.get).bind(redisClient);

// Product catalog with details: ID, name, price, and initial available quantity
const listProducts = [
  { 'itemId': 1, 'itemName': 'Suitcase 250', 'price': 50, 'initialAvailableQuantity': 4 },
  { 'itemId': 2, 'itemName': 'Suitcase 450', 'price': 100, 'initialAvailableQuantity': 10 },
  { 'itemId': 3, 'itemName': 'Suitcase 650', 'price': 350, 'initialAvailableQuantity': 2 },
  { 'itemId': 4, 'itemName': 'Suitcase 1050', 'price': 550, 'initialAvailableQuantity': 5 }
];

/**
 * Retrieve a product from the catalog by its ID.
 * @param {number} id - The ID of the product to retrieve.
 * @returns {object|null} - The product object or null if not found.
 */
function getItemById(id) {
  return listProducts.find((item) => item.itemId === id) || null;
}

/**
 * Reserve stock for a product by setting its quantity in Redis.
 * @param {number} itemId - The ID of the product.
 * @param {number} stock - The remaining stock to set in Redis.
 */
function reserveStockById(itemId, stock) {
  redisClient.set(itemId, stock);
}

/**
 * Retrieve the current reserved stock of a product from Redis.
 * @param {number} itemId - The ID of the product.
 * @returns {Promise<number|null>} - The reserved stock quantity or null if not set.
 */
async function getCurrentReservedStockById(itemId) {
  const stock = await get(itemId);
  return stock !== null ? parseInt(stock, 10) : null;
}

// Route to list all products with their details
app.get('/list_products', function(req, res) {
  res.json(listProducts);
});

// Route to retrieve a specific product's details, including current stock
app.get('/list_products/:itemId', async function(req, res) {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);

  if (item) {
    const stock = await getCurrentReservedStockById(itemId);
    const resItem = {
      itemId: item.itemId,
      itemName: item.itemName,
      price: item.price,
      initialAvailableQuantity: item.initialAvailableQuantity,
      currentQuantity: stock !== null ? stock : item.initialAvailableQuantity,
    };
    res.json(resItem);
  } else {
    res.json({ "status": "Product not found" });
  }
});

// Route to reserve a product by decrementing its stock
app.get('/reserve_product/:itemId', async function(req, res) {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);

  if (!item) {
    res.json({ "status": "Product not found" });
    return;
  }

  let currentStock = await getCurrentReservedStockById(itemId);
  currentStock = currentStock !== null ? currentStock : item.initialAvailableQuantity;

  if (currentStock > 0) {
    reserveStockById(itemId, currentStock - 1);
    res.json({ "status": "Reservation confirmed", "itemId": itemId });
  } else {
    res.json({ "status": "Not enough stock available", "itemId": itemId });
  }
});

// Start the Express server and log its listening status
const port = 1245;
app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});
