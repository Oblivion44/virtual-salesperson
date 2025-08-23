# Beauty Chatbot - Streamlit Version

An AI-powered virtual salesperson chatbot for beauty e-commerce, built with **Streamlit**, **Strand agents pattern**, **Claude 3.5**, and **NovelAI Reel** for video generation.

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
- **Interactive UI**: Beautiful Streamlit interface with real-time updates
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS styling
- **AI/ML**: Claude 3.5 (Anthropic), TextBlob for sentiment analysis
- **Video Generation**: NovelAI Reel API
- **Data Processing**: Pandas, NumPy
- **Async Operations**: asyncio, aiohttp
- **Environment**: Python 3.8+

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- API keys for Anthropic Claude and NovelAI (optional)

### Quick Start

1. **Clone and Navigate**
   ```bash
   cd beauty-chatbot-streamlit
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your API keys:
   ```env
   ANTHROPIC_API_KEY=your_claude_api_key_here
   NOVELAI_API_KEY=your_novelai_api_key_here
   NYKAA_AFFILIATE_ID=your_affiliate_id
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the App**
   Open your browser to `http://localhost:8501`

### Running in Spyder

1. **Open Spyder IDE**
2. **Navigate to the project directory**
3. **Install requirements in Spyder's console:**
   ```python
   !pip install -r requirements.txt
   ```
4. **Run the app:**
   ```python
   !streamlit run app.py
   ```
5. **The app will open in your default browser**

## 🏗️ Architecture

### Strand Agents Pattern
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
1. User interacts with Streamlit interface
2. Main chatbot analyzes intent using Claude 3.5
3. Routes to appropriate specialized agent
4. Agent processes and returns structured response
5. Streamlit updates UI with recommendations/videos/routines

## 🎯 Key Features Implementation

### 1. Interactive Chat Interface
- Real-time conversation with Bella (AI beauty consultant)
- Message history with beautiful styling
- Suggestion chips for quick responses
- User profile tracking in sidebar

### 2. Product Recommendations
```python
# Multi-factor filtering
recommendations = product_service.get_recommendations(
    user_profile={
        'category': 'skincare',
        'concerns': ['acne', 'oiliness'],
        'ageGroup': 'young_adults',
        'budget': 'under 1000'
    }
)
```

### 3. Video Tutorial Generation
```python
# Generate 10-second beauty tutorials
video_result = await video_generator.generate_video({
    'prompt': 'skincare routine demonstration',
    'style': 'tutorial',
    'duration': 10
})
```

### 4. Personalized Routines
- Step-by-step beauty routines
- Budget-aware product selection
- Customizable based on user preferences
- Visual routine display with tips

## 🔧 Configuration

### API Keys Required
- **Anthropic Claude**: For AI conversation and analysis
- **NovelAI Reel**: For video tutorial generation
- **Nykaa Affiliate** (optional): For product link tracking

### Environment Variables
```env
# Required for full functionality
ANTHROPIC_API_KEY=your_key
NOVELAI_API_KEY=your_key

# Optional
NYKAA_AFFILIATE_ID=your_id
STREAMLIT_SERVER_PORT=8501
```

## 📱 Usage Examples

### Starting a Conversation
```
User: "I have oily skin and acne problems"
Bella: "I understand you're dealing with oily skin and acne - that's very common and manageable! Let me help you find the right products..."
```

### Getting Product Recommendations
- Click "🧴 Get Products" in sidebar
- Or say "Show me product recommendations"
- View products with ratings, prices, and Nykaa links

### Building Routines
- Click "📋 Build Routine" in sidebar
- Or say "Create a skincare routine for me"
- Get step-by-step personalized routines

### Video Tutorials
- Click "🎥 Tutorials" in sidebar
- Or say "Show me how to apply skincare"
- Get video tutorials or text alternatives

## 🎨 UI Features

### Beautiful Interface
- Gradient headers and modern styling
- Chat bubbles with proper alignment
- Product cards with images and ratings
- Routine steps with visual organization
- Responsive design for all devices

### Interactive Elements
- Suggestion chips for quick responses
- Quick action buttons in sidebar
- Real-time profile updates
- Status indicators for API connections

### Sidebar Features
- User profile display
- Quick action buttons
- Settings and API status
- Reset conversation option

## 🧪 Demo Mode

The app works in **demo mode** without API keys:
- Fallback responses using rule-based logic
- Sample product recommendations
- Text tutorials instead of videos
- Full UI functionality for testing

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Add environment variables in settings
4. Deploy automatically

### Docker Deployment
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 📊 Performance Features

- **Async Operations**: Non-blocking API calls
- **Caching**: Streamlit caching for better performance
- **Error Handling**: Graceful fallbacks when APIs fail
- **Session Management**: Persistent conversation state

## 🔒 Security

- API keys stored in environment variables
- Input validation on all user messages
- No sensitive data stored in session state
- Secure API communication with proper headers

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**
   - Check `.env` file exists and has correct keys
   - Verify API keys are valid
   - App works in demo mode without keys

3. **Streamlit Issues**
   ```bash
   streamlit --version
   streamlit run app.py --server.port 8501
   ```

4. **Video Generation Fails**
   - Check NovelAI API key
   - App provides text tutorials as fallback
   - Network connectivity required

## 🔮 Future Enhancements

- Voice chat integration
- Image upload for skin analysis
- AR makeup try-on features
- Integration with more e-commerce platforms
- Advanced analytics dashboard
- Multi-language support

---

**Perfect for Spyder Users! 🐍**

This Streamlit version is specifically designed to work seamlessly in Spyder IDE:
- Easy to run with `!streamlit run app.py`
- All Python dependencies managed through pip
- Beautiful web interface that opens in your browser
- Full debugging capabilities in Spyder
- Interactive development with hot reloading

**Built with ❤️ for the beauty community and Python developers**
