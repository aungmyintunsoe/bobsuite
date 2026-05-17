
import express from 'express';
import axios from 'axios';

const app = express();
app.use(express.json());

// User API endpoint
app.get('/api/users/:id', async (req, res) => {
    try {
        const userId = req.params.id;
        const response = await axios.get(`https://jsonplaceholder.typicode.com/users/${userId}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch user' });
    }
});

// Create user endpoint
app.post('/api/users', async (req, res) => {
    try {
        const userData = req.body;
        const response = await axios.post('https://jsonplaceholder.typicode.com/users', userData);
        res.status(201).json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to create user' });
    }
});

// Rate-limited endpoint
let requestCount = 0;
const RATE_LIMIT = 100;
const TIME_WINDOW = 60000; // 1 minute

app.get('/api/limited', (req, res) => {
    requestCount++;
    if (requestCount > RATE_LIMIT) {
        return res.status(429).json({ error: 'Rate limit exceeded' });
    }
    res.json({ message: 'Success', requestCount });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
