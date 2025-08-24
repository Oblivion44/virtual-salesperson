# Beauty Chatbot - Streamlit Version with AWS Integration

An AI-powered virtual salesperson chatbot for beauty e-commerce, built with **Streamlit**, **Strand agents pattern**, **Claude 3.5**, **AWS Services**, and **NovelAI Reel** for video generation.

## 🌟 Features

### Core Chatbot Capabilities
- **Intelligent Conversation Flow**: Natural greeting and category detection (Skin/Hair/Makeup)
- **Progressive Profile Building**: Collects user information without rigid forms
- **AI-Powered Concern Analysis**: Uses Claude 3.5 for understanding beauty concerns
- **Strand Agents Architecture**: Specialized agents for different tasks
- **AWS Integration**: Enhanced features using AWS cloud services

### Specialized Agents
- **BeautyChatbot**: Main orchestrator and conversation manager
- **ConcernAnalysisAgent**: Analyzes skin/hair concerns and extracts user profile
- **RecommendationAgent**: Generates personalized product recommendations
- **EducationalAgent**: Provides tutorials and beauty education
- **RoutineAgent**: Creates personalized beauty routines

### AWS-Powered Features 🚀
- **🔬 Skin Analysis**: AWS Rekognition for facial feature and skin analysis
- **🗣️ Voice Chat**: AWS Polly for text-to-speech responses
- **📊 Sentiment Analysis**: AWS Comprehend for understanding user emotions
- **☁️ Cloud Storage**: AWS S3 for storing user images and data
- **🗄️ Profile Storage**: AWS DynamoDB for persistent user profiles
- **⚡ Serverless Functions**: AWS Lambda for advanced processing

### Advanced Features
- **Video Tutorial Generation**: NovelAI Reel integration for 10-second tutorials
- **Product Recommendations**: Smart filtering with sentiment analysis
- **Nykaa Integration**: Direct product links with affiliate tracking
- **Interactive UI**: Beautiful Streamlit interface with real-time updates
- **Responsive Design**: Works on desktop and mobile devices
- **AWS Credentials Management**: Secure credential input via Streamlit interface

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS styling
- **AI/ML**: Claude 3.5 (Anthropic), AWS Bedrock, AWS Rekognition
- **Cloud Services**: AWS (S3, Polly, Comprehend, DynamoDB, Lambda)
- **Video Generation**: NovelAI Reel API
- **Data Processing**: Pandas, NumPy
- **Async Operations**: asyncio, aiohttp
- **Environment**: Python 3.8+

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- AWS Account with appropriate permissions
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

5. **Configure AWS Credentials**
   - Open the app in your browser at `http://localhost:8501`
   - In the sidebar, expand "AWS Credentials"
   - Enter your AWS Access Key ID and Secret Access Key
   - Select your preferred AWS region
   - Click "🔗 Connect AWS"

6. **Access Enhanced Features**
   Once AWS is connected, you'll have access to:
   - Skin analysis with image upload
   - Voice chat responses
   - Cloud-based profile storage
   - Advanced sentiment analysis

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

### AWS Services Integration
```
AWS Services Layer
├── Rekognition (Image Analysis)
├── Polly (Text-to-Speech)
├── Comprehend (Sentiment Analysis)
├── S3 (File Storage)
├── DynamoDB (User Profiles)
└── Lambda (Serverless Functions)
```

### Service Layer
- **VideoGenerator**: Handles NovelAI Reel integration
- **ProductService**: Manages product data and Nykaa integration
- **AWSService**: Manages all AWS service interactions

### Data Flow
1. User interacts with Streamlit interface
2. AWS credentials validated and services initialized
3. Main chatbot analyzes intent using Claude 3.5
4. AWS services enhance analysis (sentiment, image recognition)
5. Routes to appropriate specialized agent
6. Agent processes and returns structured response
7. AWS services provide additional features (voice, storage)
8. Streamlit updates UI with recommendations/videos/routines

## 🎯 Key Features Implementation

### 1. AWS Credentials Management
```python
# Secure credential input in Streamlit sidebar
aws_access_key = st.text_input("AWS Access Key ID", type="password")
aws_secret_key = st.text_input("AWS Secret Access Key", type="password")

# Credential validation
is_valid, message = validate_aws_credentials(access_key, secret_key, region)
```

### 2. Skin Analysis with AWS Rekognition
```python
# Analyze uploaded images
response = rekognition.detect_faces(
    Image={'Bytes': image_data},
    Attributes=['ALL']
)
```

### 3. Voice Responses with AWS Polly
```python
# Generate speech from text
response = polly.synthesize_speech(
    Text=text,
    OutputFormat='mp3',
    VoiceId='Joanna',
    Engine='neural'
)
```

### 4. Sentiment Analysis with AWS Comprehend
```python
# Analyze user message sentiment
response = comprehend.detect_sentiment(
    Text=user_message,
    LanguageCode='en'
)
```

### 5. Cloud Profile Storage with DynamoDB
```python
# Store user profiles in cloud
table.put_item(
    Item={
        'user_id': user_id,
        'profile_data': profile_data,
        'timestamp': datetime.now().isoformat()
    }
)
```

## 🔧 Configuration

### AWS Services Required
- **AWS Rekognition**: For image and facial analysis
- **AWS Polly**: For text-to-speech conversion
- **AWS Comprehend**: For sentiment analysis
- **AWS S3**: For file storage (optional)
- **AWS DynamoDB**: For user profile storage (optional)

### API Keys Required
- **Anthropic Claude**: For AI conversation and analysis
- **NovelAI Reel**: For video tutorial generation
- **AWS Credentials**: Access Key ID and Secret Access Key
- **Nykaa Affiliate** (optional): For product link tracking

### Environment Variables
```env
# Required for full functionality
ANTHROPIC_API_KEY=your_key
NOVELAI_API_KEY=your_key

# AWS credentials can be entered via UI
# AWS_ACCESS_KEY_ID=your_key (optional - can use UI)
# AWS_SECRET_ACCESS_KEY=your_key (optional - can use UI)
# AWS_DEFAULT_REGION=us-east-1 (optional - can use UI)

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

### Using AWS Features

#### Skin Analysis
1. Click "📸 Analyze Skin" in AWS Features section
2. Upload a clear photo of your face
3. Click "🔬 Analyze Skin"
4. Get AI-powered skin analysis and recommendations

#### Voice Chat
1. Click "🗣️ Voice Chat" in AWS Features section
2. Select your preferred voice (Joanna, Amy, Emma, Olivia)
3. All responses will include audio playback
4. Test voice with sample text

#### Profile Storage
- Say "Save my profile to cloud"
- Your beauty profile gets stored in AWS DynamoDB
- Access from any device with same user ID

## 🎨 UI Features

### Beautiful Interface
- Gradient headers and modern styling
- Chat bubbles with proper alignment
- Product cards with images and ratings
- Routine steps with visual organization
- AWS service status indicators
- Responsive design for all devices

### AWS Integration UI
- **Credentials Panel**: Secure input for AWS credentials
- **Service Status**: Real-time AWS connection status
- **Feature Toggles**: Enable/disable AWS features
- **Upload Interface**: Drag-and-drop image upload
- **Voice Controls**: Voice selection and testing
- **Progress Indicators**: Real-time processing status

### Interactive Elements
- Suggestion chips for quick responses
- Quick action buttons in sidebar
- AWS-powered feature buttons
- Real-time profile updates
- Status indicators for all services
- Reset conversation option

### Sidebar Features
- **AWS Configuration**: Credential management and service status
- **User Profile**: Real-time profile display
- **Quick Actions**: Standard beauty consultation features
- **AWS Features**: Enhanced cloud-powered features
- **Settings**: API status and configuration options

## 🧪 Demo Mode

The app works in **demo mode** without AWS credentials:
- Fallback responses using rule-based logic
- Sample product recommendations
- Text tutorials instead of videos
- Full UI functionality for testing
- AWS features show informational messages

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Add environment variables in settings (optional for AWS)
4. Users enter AWS credentials via UI
5. Deploy automatically

### AWS Deployment
```bash
# Deploy to AWS EC2 or ECS
# Configure IAM roles for service access
# Use AWS Systems Manager for credential management
```

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

- **Async Operations**: Non-blocking API calls to AWS services
- **Caching**: Streamlit caching for better performance
- **Error Handling**: Graceful fallbacks when AWS services fail
- **Session Management**: Persistent conversation state
- **Connection Pooling**: Efficient AWS service connections
- **Lazy Loading**: AWS services initialized only when needed

## 🔒 Security

- AWS credentials entered via secure password fields
- Credentials stored only in session state (not persistent)
- API keys stored in environment variables
- Input validation on all user messages
- Secure AWS API communication with proper headers
- No sensitive data logged or stored permanently
- IAM best practices recommended for AWS access

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/aws-integration`
3. Commit changes: `git commit -am 'Add AWS integration'`
4. Push to branch: `git push origin feature/aws-integration`
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **AWS Connection Issues**
   - Verify AWS credentials are correct
   - Check IAM permissions for required services
   - Ensure selected region supports all services
   - Check AWS service quotas and limits

3. **API Key Issues**
   - Check `.env` file exists and has correct keys
   - Verify API keys are valid
   - App works in demo mode without keys

4. **Streamlit Issues**
   ```bash
   streamlit --version
   streamlit run app.py --server.port 8501
   ```

5. **AWS Service Errors**
   - Check service availability in selected region
   - Verify IAM permissions for each service
   - Monitor AWS CloudWatch for service issues
   - Use AWS CLI to test service access

### AWS Permissions Required

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "rekognition:DetectFaces",
                "polly:SynthesizeSpeech",
                "comprehend:DetectSentiment",
                "s3:GetObject",
                "s3:PutObject",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

## 🔮 Future Enhancements

- **Advanced AWS Features**:
  - AWS Bedrock integration for enhanced AI models
  - AWS Lambda functions for complex processing
  - AWS API Gateway for scalable deployment
  - AWS Cognito for user authentication

- **Enhanced Beauty Features**:
  - Real-time skin condition monitoring
  - AR makeup try-on with AWS services
  - Personalized product recommendations using ML
  - Integration with more e-commerce platforms

- **Technical Improvements**:
  - Multi-language support with AWS Translate
  - Advanced analytics dashboard
  - Mobile app with AWS Amplify
  - Voice commands with AWS Lex

---

**Perfect for AWS-Powered Beauty Consultations! ☁️✨**

This enhanced version combines the power of AI beauty consultation with AWS cloud services:
- **Secure**: Enterprise-grade AWS security
- **Scalable**: Cloud-native architecture
- **Intelligent**: Multiple AI services working together
- **User-Friendly**: Simple credential management via UI
- **Professional**: Production-ready AWS integration

**Built with ❤️ for the beauty community, Python developers, and AWS enthusiasts**
