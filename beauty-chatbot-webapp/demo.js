// Demo script to test the Beauty Chatbot without API keys
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(express.static('public'));
app.use(express.json());

// Store demo chat sessions
const demoSessions = new Map();

// Demo responses for testing
const demoResponses = {
  greeting: [
    "Hi there! I'm Bella, your personal beauty consultant! ✨ I'm here to help you discover amazing products for your skin, hair, or makeup needs. What brings you here today?",
    "Hello beautiful! 💄 I'm Bella, and I'm excited to help you find the perfect beauty products! Are you looking for skincare, haircare, or makeup solutions?"
  ],
  skincare: [
    "I understand you're interested in skincare! That's wonderful - taking care of your skin is so important. Could you tell me a bit about your current skin concerns? For example, do you deal with dryness, oiliness, acne, or sensitivity?",
    "Skincare is my passion! ✨ To give you the best recommendations, I'd love to know more about your skin. What's your biggest skin concern right now?"
  ],
  haircare: [
    "Hair care is such an important part of your beauty routine! 💇‍♀️ Tell me about your hair - is it dry, oily, damaged, or do you have specific styling concerns?",
    "I love helping with hair concerns! What's going on with your hair that you'd like to address? Dryness, damage, lack of volume, or something else?"
  ],
  makeup: [
    "Makeup is so fun! 💄 Are you looking for everyday makeup tips, special occasion looks, or help with specific products like foundation, eyeshadow, or lipstick?",
    "I'm excited to help with your makeup journey! What aspect of makeup would you like to focus on today?"
  ],
  products: [
    "Based on what you've told me, I have some amazing product recommendations! 🛍️ I've found some highly-rated products that would be perfect for your needs. They're all available on Nykaa with great reviews!",
    "Perfect! I've curated some fantastic products just for you! These are all bestsellers with amazing reviews from people with similar concerns."
  ],
  routine: [
    "I'd love to create a personalized routine for you! 📋 Based on your concerns, here's a simple but effective routine that will help you achieve your beauty goals. I'll break it down step by step so it's easy to follow.",
    "Let me design the perfect routine for you! This will be customized based on everything you've shared with me."
  ],
  tutorial: [
    "I can create a tutorial video for you! 🎥 While I'm generating your personalized tutorial, here are the key steps you should know...",
    "Great idea! Let me prepare a tutorial that's perfect for your needs. This will show you exactly how to achieve the best results."
  ]
};

const demoSuggestions = {
  initial: ['Skincare help', 'Hair concerns', 'Makeup advice', 'Build a routine'],
  skincare: ['I have oily skin', 'I have dry skin', 'I have acne problems', 'I have sensitive skin'],
  haircare: ['My hair is damaged', 'My hair is too oily', 'My hair is dry and frizzy', 'I want volume'],
  makeup: ['Everyday makeup', 'Special occasion look', 'Foundation help', 'Eye makeup tips'],
  followup: ['Show me products', 'Create a routine', 'I want tutorials', 'Tell me more']
};

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    mode: 'demo',
    message: 'Running in demo mode - no API keys required',
    timestamp: new Date().toISOString() 
  });
});

// Socket.IO connection handling
io.on('connection', (socket) => {
  console.log(`Demo user connected: ${socket.id}`);
  
  // Initialize demo session
  demoSessions.set(socket.id, {
    userId: socket.id,
    step: 'greeting',
    category: null,
    messageCount: 0
  });

  // Handle chat messages
  socket.on('chat_message', async (data) => {
    try {
      const session = demoSessions.get(socket.id);
      const { message } = data;
      
      session.messageCount++;
      
      // Simple intent detection for demo
      let responseType = 'greeting';
      let suggestions = demoSuggestions.initial;
      
      const messageLower = message.toLowerCase();
      
      if (messageLower.includes('skin') || messageLower.includes('acne') || messageLower.includes('dry') || messageLower.includes('oily')) {
        responseType = 'skincare';
        session.category = 'skincare';
        suggestions = demoSuggestions.skincare;
      } else if (messageLower.includes('hair') || messageLower.includes('frizz') || messageLower.includes('damage')) {
        responseType = 'haircare';
        session.category = 'haircare';
        suggestions = demoSuggestions.haircare;
      } else if (messageLower.includes('makeup') || messageLower.includes('foundation') || messageLower.includes('lipstick')) {
        responseType = 'makeup';
        session.category = 'makeup';
        suggestions = demoSuggestions.makeup;
      } else if (messageLower.includes('product') || messageLower.includes('recommend')) {
        responseType = 'products';
        suggestions = demoSuggestions.followup;
      } else if (messageLower.includes('routine')) {
        responseType = 'routine';
        suggestions = demoSuggestions.followup;
      } else if (messageLower.includes('tutorial') || messageLower.includes('video') || messageLower.includes('how to')) {
        responseType = 'tutorial';
        suggestions = demoSuggestions.followup;
      } else if (session.messageCount > 1) {
        responseType = session.category || 'skincare';
        suggestions = demoSuggestions.followup;
      }

      // Get random response
      const responses = demoResponses[responseType] || demoResponses.greeting;
      const response = responses[Math.floor(Math.random() * responses.length)];
      
      // Update session
      demoSessions.set(socket.id, session);

      // Simulate thinking delay
      setTimeout(() => {
        socket.emit('bot_response', {
          message: response,
          type: responseType,
          suggestions: suggestions
        });

        // Simulate product recommendations
        if (responseType === 'products') {
          setTimeout(() => {
            socket.emit('product_recommendations', {
              products: getDemoProducts(session.category)
            });
          }, 1000);
        }

        // Simulate video generation
        if (responseType === 'tutorial') {
          setTimeout(() => {
            socket.emit('video_generation_started', {
              message: 'Creating your personalized tutorial...'
            });
            
            setTimeout(() => {
              socket.emit('video_error', {
                message: 'Demo mode: Video generation requires API keys. Here\'s a text tutorial instead!'
              });
            }, 3000);
          }, 500);
        }
      }, 1000 + Math.random() * 1000); // 1-2 second delay

    } catch (error) {
      console.error('Demo error:', error);
      socket.emit('error', { message: 'Demo mode error - please try again!' });
    }
  });

  // Handle video generation requests
  socket.on('generate_video', (data) => {
    socket.emit('video_generation_started', { 
      message: 'Demo mode: Generating tutorial...' 
    });
    
    setTimeout(() => {
      socket.emit('video_error', {
        message: 'Demo mode: Video generation requires NovelAI API key. Configure your .env file to enable video features!'
      });
    }, 2000);
  });

  // Handle disconnect
  socket.on('disconnect', () => {
    console.log(`Demo user disconnected: ${socket.id}`);
    demoSessions.delete(socket.id);
  });
});

function getDemoProducts(category = 'skincare') {
  const products = {
    skincare: [
      {
        name: 'Cetaphil Gentle Skin Cleanser',
        brand: 'Cetaphil',
        price: '₹599',
        rating: 4.5,
        reviews: 1250,
        image: '/images/placeholder-product.jpg',
        nykaaUrl: 'https://www.nykaa.com/cetaphil-gentle-skin-cleanser'
      },
      {
        name: 'The Ordinary Hyaluronic Acid 2% + B5',
        brand: 'The Ordinary',
        price: '₹849',
        rating: 4.7,
        reviews: 2100,
        image: '/images/placeholder-product.jpg',
        nykaaUrl: 'https://www.nykaa.com/the-ordinary-hyaluronic-acid'
      }
    ],
    haircare: [
      {
        name: 'L\'Oréal Paris Total Repair 5 Shampoo',
        brand: 'L\'Oréal Paris',
        price: '₹399',
        rating: 4.4,
        reviews: 756,
        image: '/images/placeholder-product.jpg',
        nykaaUrl: 'https://www.nykaa.com/loreal-total-repair-shampoo'
      }
    ],
    makeup: [
      {
        name: 'Maybelline Fit Me Foundation',
        brand: 'Maybelline',
        price: '₹499',
        rating: 4.3,
        reviews: 890,
        image: '/images/placeholder-product.jpg',
        nykaaUrl: 'https://www.nykaa.com/maybelline-fit-me-foundation'
      }
    ]
  };

  return products[category] || products.skincare;
}

const PORT = process.env.PORT || 3001;
server.listen(PORT, () => {
  console.log(`🎭 Beauty Chatbot DEMO running on port ${PORT}`);
  console.log(`📱 Access the demo at http://localhost:${PORT}`);
  console.log(`ℹ️  This is demo mode - no API keys required!`);
  console.log(`🔑 To enable full features, configure API keys in .env and run: npm start`);
});
