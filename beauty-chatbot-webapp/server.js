const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const BeautyChatbot = require('./src/agents/BeautyChatbot');
const VideoGenerator = require('./src/services/VideoGenerator');
const ProductService = require('./src/services/ProductService');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Initialize services
const chatbot = new BeautyChatbot();
const videoGenerator = new VideoGenerator();
const productService = new ProductService();

// Store active chat sessions
const chatSessions = new Map();

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Socket.IO connection handling
io.on('connection', (socket) => {
  console.log(`User connected: ${socket.id}`);
  
  // Initialize chat session
  chatSessions.set(socket.id, {
    userId: socket.id,
    profile: {},
    conversationHistory: [],
    currentStep: 'greeting',
    preferences: {}
  });

  // Handle chat messages
  socket.on('chat_message', async (data) => {
    try {
      const session = chatSessions.get(socket.id);
      const { message, messageType = 'text' } = data;

      // Add user message to history
      session.conversationHistory.push({
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
      });

      // Process message through chatbot
      const response = await chatbot.processMessage(message, session);
      
      // Add bot response to history
      session.conversationHistory.push({
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString(),
        data: response.data || {}
      });

      // Update session
      chatSessions.set(socket.id, session);

      // Send response back to client
      socket.emit('bot_response', {
        message: response.message,
        type: response.type || 'text',
        data: response.data || {},
        suggestions: response.suggestions || []
      });

      // Handle special response types
      if (response.type === 'product_recommendations') {
        // Fetch product details
        const products = await productService.getProductDetails(response.data.productIds);
        socket.emit('product_recommendations', { products });
      }

      if (response.type === 'video_tutorial_request') {
        // Generate educational video
        const videoData = await videoGenerator.generateTutorial(response.data.topic);
        socket.emit('video_content', videoData);
      }

    } catch (error) {
      console.error('Error processing message:', error);
      socket.emit('error', { message: 'Sorry, I encountered an error. Please try again.' });
    }
  });

  // Handle video generation requests
  socket.on('generate_video', async (data) => {
    try {
      const { prompt, style = 'tutorial', duration = 10 } = data;
      
      socket.emit('video_generation_started', { message: 'Generating your video tutorial...' });
      
      const videoResult = await videoGenerator.generateVideo({
        prompt,
        style,
        duration,
        userId: socket.id
      });

      socket.emit('video_generated', videoResult);
    } catch (error) {
      console.error('Video generation error:', error);
      socket.emit('video_error', { message: 'Failed to generate video. Please try again.' });
    }
  });

  // Handle product search
  socket.on('search_products', async (data) => {
    try {
      const { query, filters = {} } = data;
      const results = await productService.searchProducts(query, filters);
      socket.emit('search_results', { products: results });
    } catch (error) {
      console.error('Product search error:', error);
      socket.emit('search_error', { message: 'Failed to search products.' });
    }
  });

  // Handle disconnect
  socket.on('disconnect', () => {
    console.log(`User disconnected: ${socket.id}`);
    chatSessions.delete(socket.id);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`🚀 Beauty Chatbot Server running on port ${PORT}`);
  console.log(`📱 Access the app at http://localhost:${PORT}`);
});
