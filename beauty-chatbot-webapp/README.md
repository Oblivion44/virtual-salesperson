# Beauty Chatbot Web App

An AI-powered virtual salesperson chatbot for beauty e-commerce, built with Strand agents pattern, Claude 3.5, and NovelAI Reel for video generation.

## 🌟 Features

### Core Chatbot Capabilities
- **Intelligent Conversation Flow**: Natural greeting and category detection (Skin/Hair/Makeup)
- **Progressive Profile Building**: Collects user information without rigid forms
- **AI-Powered Concern Analysis**: Uses Claude 3.5 for understanding beauty concerns
- **Strand Agents Architecture**: Specialized agents for different tasks

### Specialized Agents
- **BeautyChatbot**: Main orchestrator and conversation manager
- **ConcernAnalysisAgent**: Analyzes skin/hair concerns and extracts user profile
- **RecommendationAgent**: Generates personalized product recommendations
- **EducationalAgent**: Provides tutorials and beauty education
- **RoutineAgent**: Creates personalized beauty routines

### Advanced Features
- **Video Tutorial Generation**: NovelAI Reel integration for 10-second tutorials
- **Product Recommendations**: Smart filtering with sentiment analysis
- **Nykaa Integration**: Direct product links with affiliate tracking
- **Real-time Chat**: Socket.IO for instant messaging
- **Responsive Design**: Mobile-friendly interface

## 🛠️ Technology Stack

- **Backend**: Node.js, Express.js, Socket.IO
- **AI/ML**: Claude 3.5 (Anthropic), Natural Language Processing
- **Video Generation**: NovelAI Reel API
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Data Processing**: CSV parsing, Sentiment analysis
- **Real-time**: WebSocket connections

## 📦 Installation

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- API keys for Anthropic Claude and NovelAI

### Setup Steps

1. **Clone and Navigate**
   ```bash
   cd beauty-chatbot-webapp
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your API keys:
   ```env
   ANTHROPIC_API_KEY=your_claude_api_key_here
   NOVELAI_API_KEY=your_novelai_api_key_here
   PORT=3000
   NYKAA_AFFILIATE_ID=your_affiliate_id
   ```

4. **Create Required Directories**
   ```bash
   mkdir -p public/videos public/images
   ```

5. **Start the Server**
   ```bash
   npm start
   # or for development
   npm run dev
   ```

6. **Access the App**
   Open http://localhost:3000 in your browser

## 🏗️ Architecture

### Strand Agents Pattern
The application uses a specialized agent architecture where each agent handles specific aspects of the beauty consultation:

```
BeautyChatbot (Main Orchestrator)
├── ConcernAnalysisAgent (Profile & Concern Analysis)
├── RecommendationAgent (Product Suggestions)
├── EducationalAgent (Tutorials & Education)
└── RoutineAgent (Routine Building)
```

### Service Layer
- **VideoGenerator**: Handles NovelAI Reel integration
- **ProductService**: Manages product data and Nykaa integration

### Data Flow
1. User sends message via WebSocket
2. Main chatbot analyzes intent
3. Routes to appropriate specialized agent
4. Agent processes and returns structured response
5. Frontend updates UI with recommendations/videos

## 🎯 Key Features Implementation

### 1. Intelligent Conversation
- Natural language understanding with Claude 3.5
- Context-aware responses based on conversation history
- Progressive information gathering

### 2. Video Tutorial Generation
```javascript
// Generate 10-second beauty tutorials
const videoResult = await videoGenerator.generateVideo({
  prompt: "skincare routine demonstration",
  style: 'tutorial',
  duration: 10
});
```

### 3. Product Recommendations
- Multi-factor filtering (concerns, age, budget, skin type)
- Sentiment analysis of reviews
- Direct Nykaa.com integration

### 4. Personalized Routines
- Step-by-step beauty routines
- Budget-aware product selection
- Customizable based on user preferences

## 🔧 Configuration

### API Keys Required
- **Anthropic Claude**: For AI conversation and analysis
- **NovelAI Reel**: For video tutorial generation
- **Nykaa Affiliate** (optional): For product link tracking

### Environment Variables
```env
# Required
ANTHROPIC_API_KEY=your_key
NOVELAI_API_KEY=your_key

# Optional
NYKAA_AFFILIATE_ID=your_id
PORT=3000
NODE_ENV=development
```

## 📱 Usage Examples

### Starting a Conversation
```
User: "I have oily skin and acne problems"
Bella: "I understand you're dealing with oily skin and acne - that's actually very common and totally manageable! Let me help you find the right products..."
```

### Requesting Video Tutorials
```
User: "Show me how to apply skincare products"
Bella: "I'll create a personalized tutorial for you!"
[Generates 10-second video via NovelAI Reel]
```

### Building Routines
```
User: "Create a morning skincare routine for me"
Bella: "Perfect! Based on your oily skin and acne concerns, here's your personalized morning routine..."
```

## 🧪 Testing

### Manual Testing
1. Start the server: `npm start`
2. Open browser to `http://localhost:3000`
3. Test conversation flows:
   - Greeting and category detection
   - Concern analysis
   - Product recommendations
   - Video generation
   - Routine building

### API Testing
```bash
# Test health endpoint
curl http://localhost:3000/api/health
```

## 🚀 Deployment

### Local Development
```bash
npm run dev  # Uses nodemon for auto-restart
```

### Production
```bash
npm start
```

### Environment Setup
- Ensure all API keys are configured
- Set `NODE_ENV=production`
- Configure proper CORS settings for your domain

## 📊 Performance Considerations

- **Video Generation**: Can take 30-120 seconds depending on NovelAI load
- **Product Search**: Optimized with in-memory filtering
- **Real-time Chat**: WebSocket connections for instant responses
- **Fallback Handling**: Text tutorials when video generation fails

## 🔒 Security

- API keys stored in environment variables
- Input validation on all user messages
- CORS configuration for production
- No sensitive data stored in frontend

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
1. Check the console logs for error messages
2. Verify API keys are correctly configured
3. Ensure all dependencies are installed
4. Check network connectivity for API calls

## 🔮 Future Enhancements

- Voice chat integration
- Image analysis for skin concerns
- AR makeup try-on features
- Integration with more e-commerce platforms
- Advanced analytics and user insights

---

**Built with ❤️ for the beauty community**

*This chatbot represents the future of personalized beauty consultation, combining AI intelligence with human-like conversation to help users discover their perfect beauty routine.*
