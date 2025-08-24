import streamlit as st
import asyncio
import json
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Import our custom agents and services
from src.agents.beauty_chatbot import BeautyChatbot
from src.agents.concern_analysis_agent import ConcernAnalysisAgent
from src.agents.recommendation_agent import RecommendationAgent
from src.agents.educational_agent import EducationalAgent
from src.agents.routine_agent import RoutineAgent
from src.services.video_generator import VideoGenerator
from src.services.product_service import ProductService

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Bella - AI Beauty Consultant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #ff6b6b, #ffa726);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        margin-left: auto;
    }
    
    .bot-message {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        color: #495057;
    }
    
    .product-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .suggestion-chip {
        background: #667eea;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        display: inline-block;
        cursor: pointer;
    }
    
    .routine-step {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .status-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background: #4caf50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    if 'conversation_step' not in st.session_state:
        st.session_state.conversation_step = 'greeting'
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = BeautyChatbot()
    if 'product_service' not in st.session_state:
        st.session_state.product_service = ProductService()
    if 'video_generator' not in st.session_state:
        st.session_state.video_generator = VideoGenerator()
    # AWS credentials
    if 'aws_access_key' not in st.session_state:
        st.session_state.aws_access_key = ''
    if 'aws_secret_key' not in st.session_state:
        st.session_state.aws_secret_key = ''
    if 'aws_region' not in st.session_state:
        st.session_state.aws_region = 'us-east-1'
    if 'aws_connected' not in st.session_state:
        st.session_state.aws_connected = False
    if 'aws_services' not in st.session_state:
        st.session_state.aws_services = {}

def validate_aws_credentials(access_key, secret_key, region):
    """Validate AWS credentials by making a simple API call"""
    try:
        # Create a session with the provided credentials
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        
        # Test connection with STS (Security Token Service)
        sts_client = session.client('sts')
        sts_client.get_caller_identity()
        
        return True, "AWS credentials validated successfully!"
    except NoCredentialsError:
        return False, "Invalid AWS credentials provided."
    except ClientError as e:
        return False, f"AWS connection error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def initialize_aws_services():
    """Initialize AWS services with validated credentials"""
    if not st.session_state.aws_connected:
        return
    
    try:
        # Create session with stored credentials
        session = boto3.Session(
            aws_access_key_id=st.session_state.aws_access_key,
            aws_secret_access_key=st.session_state.aws_secret_key,
            region_name=st.session_state.aws_region
        )
        
        # Initialize commonly used AWS services
        st.session_state.aws_services = {
            's3': session.client('s3'),
            'bedrock': session.client('bedrock-runtime'),
            'rekognition': session.client('rekognition'),
            'polly': session.client('polly'),
            'comprehend': session.client('comprehend'),
            'lambda': session.client('lambda'),
            'dynamodb': session.resource('dynamodb')
        }
        
        return True
    except Exception as e:
        st.error(f"Failed to initialize AWS services: {str(e)}")
        return False

def get_aws_service_status():
    """Get status of AWS services"""
    if not st.session_state.aws_connected:
        return "🔴 Not Connected"
    
    try:
        # Test a simple service call
        sts_client = boto3.client(
            'sts',
            aws_access_key_id=st.session_state.aws_access_key,
            aws_secret_access_key=st.session_state.aws_secret_key,
            region_name=st.session_state.aws_region
        )
        sts_client.get_caller_identity()
        return "🟢 Connected"
    except:
        return "🟡 Connection Issues"

def main():
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>✨ Bella - AI Beauty Consultant</h1>
        <p>Your personal beauty expert powered by AI & AWS</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status indicators
    api_status = "🟢 Connected" if os.getenv('ANTHROPIC_API_KEY') else "🟡 Demo Mode"
    aws_status = get_aws_service_status()
    st.markdown(f'<div class="status-indicator">Claude: {api_status} | AWS: {aws_status}</div>', unsafe_allow_html=True)
    
    # Sidebar for user profile and controls
    with st.sidebar:
        st.header("🔐 AWS Configuration")
        
        # AWS Credentials Section
        with st.expander("AWS Credentials", expanded=not st.session_state.aws_connected):
            aws_access_key = st.text_input(
                "AWS Access Key ID",
                value=st.session_state.aws_access_key,
                type="password",
                help="Enter your AWS Access Key ID"
            )
            
            aws_secret_key = st.text_input(
                "AWS Secret Access Key",
                value=st.session_state.aws_secret_key,
                type="password",
                help="Enter your AWS Secret Access Key"
            )
            
            aws_region = st.selectbox(
                "AWS Region",
                options=[
                    'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
                    'eu-west-1', 'eu-west-2', 'eu-central-1',
                    'ap-south-1', 'ap-southeast-1', 'ap-southeast-2',
                    'ap-northeast-1', 'ap-northeast-2'
                ],
                index=0 if st.session_state.aws_region == 'us-east-1' else 0,
                help="Select your preferred AWS region"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔗 Connect AWS", use_container_width=True):
                    if aws_access_key and aws_secret_key:
                        with st.spinner("Validating AWS credentials..."):
                            is_valid, message = validate_aws_credentials(aws_access_key, aws_secret_key, aws_region)
                            
                            if is_valid:
                                st.session_state.aws_access_key = aws_access_key
                                st.session_state.aws_secret_key = aws_secret_key
                                st.session_state.aws_region = aws_region
                                st.session_state.aws_connected = True
                                initialize_aws_services()
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                    else:
                        st.error("Please provide both Access Key ID and Secret Access Key")
            
            with col2:
                if st.button("🔌 Disconnect", use_container_width=True):
                    st.session_state.aws_access_key = ''
                    st.session_state.aws_secret_key = ''
                    st.session_state.aws_connected = False
                    st.session_state.aws_services = {}
                    st.success("Disconnected from AWS")
                    st.rerun()
        
        # AWS Services Status
        if st.session_state.aws_connected:
            st.success("✅ AWS Connected")
            st.info(f"Region: {st.session_state.aws_region}")
            
            # Show available services
            with st.expander("Available AWS Services"):
                services = [
                    "🪣 S3 (Storage)",
                    "🧠 Bedrock (AI Models)",
                    "👁️ Rekognition (Image Analysis)",
                    "🗣️ Polly (Text-to-Speech)",
                    "📝 Comprehend (Text Analysis)",
                    "⚡ Lambda (Functions)",
                    "🗄️ DynamoDB (Database)"
                ]
                for service in services:
                    st.write(f"• {service}")
        else:
            st.warning("⚠️ AWS Not Connected")
            st.info("Connect AWS for enhanced features like image analysis and cloud storage")
        
        st.divider()
        
        st.header("👤 Your Beauty Profile")
        
        # Display current profile
        if st.session_state.user_profile:
            st.json(st.session_state.user_profile)
        else:
            st.info("Start chatting to build your profile!")
        
        st.divider()
        
        # Quick actions
        st.header("🚀 Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧴 Get Products", use_container_width=True):
                handle_quick_action("Show me product recommendations")
        
        with col2:
            if st.button("📋 Build Routine", use_container_width=True):
                handle_quick_action("Create a beauty routine for me")
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🎥 Tutorials", use_container_width=True):
                handle_quick_action("Show me beauty tutorials")
        
        with col4:
            if st.button("🔄 Reset Chat", use_container_width=True):
                reset_conversation()
        
        # AWS-powered features (only show if connected)
        if st.session_state.aws_connected:
            st.divider()
            st.header("☁️ AWS Features")
            
            col5, col6 = st.columns(2)
            with col5:
                if st.button("📸 Analyze Skin", use_container_width=True):
                    handle_quick_action("I want to analyze my skin using AI")
            
            with col6:
                if st.button("🗣️ Voice Chat", use_container_width=True):
                    handle_quick_action("Enable voice chat mode")
        
        st.divider()
        
        # Settings
        st.header("⚙️ Settings")
        
        # API Key status
        if os.getenv('ANTHROPIC_API_KEY'):
            st.success("✅ Claude API Connected")
        else:
            st.warning("⚠️ Running in Demo Mode")
            st.info("Add ANTHROPIC_API_KEY to .env for full features")
        
        if os.getenv('NOVELAI_API_KEY'):
            st.success("✅ NovelAI Connected")
        else:
            st.info("Add NOVELAI_API_KEY for video generation")
    
    # Main chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            display_message(message)
    
    # Input area
    st.divider()
    
    # Suggestion chips
    if st.session_state.conversation_step == 'greeting':
        st.markdown("**💡 Try these suggestions:**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🌿 Skincare Help", key="skin_help"):
                handle_user_input("I need skincare help")
        
        with col2:
            if st.button("💇‍♀️ Hair Concerns", key="hair_help"):
                handle_user_input("I have hair concerns")
        
        with col3:
            if st.button("💄 Makeup Advice", key="makeup_help"):
                handle_user_input("I want makeup advice")
        
        with col4:
            if st.button("📅 Build Routine", key="routine_help"):
                handle_user_input("Build me a routine")
    
    # Chat input
    user_input = st.chat_input("Ask me about skincare, haircare, or makeup...")
    
    if user_input:
        handle_user_input(user_input)
    
    # Welcome message for new users
    if not st.session_state.messages:
        welcome_message = {
            'role': 'assistant',
            'content': "Hi there! I'm Bella, your personal beauty consultant! ✨ I'm here to help you discover amazing products for your skin, hair, and makeup needs. What brings you here today?",
            'timestamp': datetime.now().isoformat(),
            'type': 'greeting'
        }
        st.session_state.messages.append(welcome_message)
        st.rerun()

def handle_user_input(user_input):
    """Handle user input and generate bot response"""
    # Add user message
    user_message = {
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now().isoformat()
    }
    st.session_state.messages.append(user_message)
    
    # Generate bot response
    with st.spinner("Bella is thinking..."):
        try:
            # Create session data for the chatbot
            session_data = {
                'userId': st.session_state.session_id,
                'profile': st.session_state.user_profile,
                'conversationHistory': st.session_state.messages,
                'currentStep': st.session_state.conversation_step,
                'preferences': {}
            }
            
            # Process message through chatbot
            response = asyncio.run(st.session_state.chatbot.process_message(user_input, session_data))
            
            # Update session state
            st.session_state.user_profile = session_data.get('profile', {})
            st.session_state.conversation_step = session_data.get('currentStep', 'general')
            
            # Add bot response
            bot_message = {
                'role': 'assistant',
                'content': response.get('message', 'I apologize, but I encountered an issue. Could you please try again?'),
                'timestamp': datetime.now().isoformat(),
                'type': response.get('type', 'text'),
                'data': response.get('data', {}),
                'suggestions': response.get('suggestions', [])
            }
            st.session_state.messages.append(bot_message)
            
            # Handle special response types
            if response.get('type') == 'product_recommendations':
                handle_product_recommendations(response.get('data', {}))
            elif response.get('type') == 'video_tutorial_request':
                handle_video_request(response.get('data', {}))
            elif response.get('type') == 'routine_created':
                handle_routine_display(response.get('data', {}))
            
        except Exception as e:
            error_message = {
                'role': 'assistant',
                'content': f"I'm sorry, I encountered an error: {str(e)}. Please try again!",
                'timestamp': datetime.now().isoformat(),
                'type': 'error'
            }
            st.session_state.messages.append(error_message)
    
    st.rerun()

def handle_quick_action(action_text):
    """Handle quick action buttons"""
    handle_user_input(action_text)

def display_message(message):
    """Display a chat message with proper styling"""
    role = message['role']
    content = message['content']
    msg_type = message.get('type', 'text')
    data = message.get('data', {})
    
    if role == 'user':
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>✨ Bella:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
        
        # Handle special message types
        if msg_type == 'product_recommendations' and data:
            display_product_recommendations(data)
        elif msg_type == 'routine_created' and data:
            display_routine(data)
        elif msg_type == 'video_tutorial_request':
            display_video_section(data)
        elif msg_type == 'aws_skin_analysis_request':
            display_skin_analysis_upload()
        elif msg_type == 'voice_chat_enabled':
            display_voice_chat_controls()
        
        # Display suggestions
        suggestions = message.get('suggestions', [])
        if suggestions:
            display_suggestions(suggestions)

def display_skin_analysis_upload():
    """Display skin analysis upload interface"""
    st.markdown("### 📸 Skin Analysis with AWS Rekognition")
    
    uploaded_file = st.file_uploader(
        "Upload a clear photo of your face",
        type=['jpg', 'jpeg', 'png'],
        help="For best results, use a well-lit photo with your face clearly visible"
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", width=200)
        
        with col2:
            if st.button("🔬 Analyze Skin", key="analyze_skin_btn"):
                with st.spinner("Analyzing your skin with AWS Rekognition..."):
                    # Read image data
                    image_data = uploaded_file.read()
                    
                    # Analyze with AWS
                    insights, message = analyze_skin_with_aws(image_data)
                    
                    if insights:
                        st.success("✅ Analysis Complete!")
                        
                        # Display results
                        st.markdown("#### 🔍 Analysis Results")
                        st.info(f"Faces detected: {insights['faces_detected']}")
                        st.write(insights['analysis'])
                        
                        st.markdown("#### 💡 Recommendations")
                        for rec in insights['recommendations']:
                            st.write(f"• {rec}")
                        
                        # Add analysis to chat
                        analysis_message = {
                            'role': 'assistant',
                            'content': f"Great! I've analyzed your photo using AWS Rekognition. {insights['analysis']} Based on the analysis, here are my recommendations for your skincare routine.",
                            'timestamp': datetime.now().isoformat(),
                            'type': 'aws_analysis_result',
                            'data': insights
                        }
                        st.session_state.messages.append(analysis_message)
                    else:
                        st.error(f"Analysis failed: {message}")

def display_voice_chat_controls():
    """Display voice chat controls"""
    st.markdown("### 🗣️ Voice Chat Mode")
    st.info("Voice responses are now enabled using AWS Polly!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        voice_option = st.selectbox(
            "Select Voice",
            options=['Joanna', 'Amy', 'Emma', 'Olivia'],
            help="Choose your preferred voice for responses"
        )
    
    with col2:
        if st.button("🔊 Test Voice", key="test_voice_btn"):
            test_text = "Hello! I'm Bella, your AI beauty consultant. How can I help you today?"
            with st.spinner("Generating voice sample..."):
                audio_data, message = generate_voice_response(test_text)
                if audio_data:
                    st.audio(audio_data, format='audio/mp3')
                    st.success("Voice test successful!")
                else:
                    st.error(f"Voice generation failed: {message}")

def display_suggestions(suggestions):
    """Display suggestion chips"""
    st.markdown("**💡 Suggestions:**")
    cols = st.columns(min(len(suggestions), 4))
    
    for i, suggestion in enumerate(suggestions[:4]):
        with cols[i % 4]:
            if st.button(suggestion, key=f"suggestion_{i}_{len(st.session_state.messages)}"):
                handle_user_input(suggestion)

def display_product_recommendations(data):
    """Display product recommendations"""
    st.markdown("### 🛍️ Recommended Products")
    
    # Get product details
    products = st.session_state.product_service.get_sample_products()[:3]
    
    for product in products:
        with st.container():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Placeholder for product image
                st.image("https://via.placeholder.com/150x150?text=Product", width=150)
            
            with col2:
                st.markdown(f"""
                <div class="product-card">
                    <h4>{product['name']}</h4>
                    <p><strong>Brand:</strong> {product['brand']}</p>
                    <p><strong>Price:</strong> ₹{product['price']}</p>
                    <p><strong>Rating:</strong> {'⭐' * int(product['rating'])} ({product['rating']}/5)</p>
                    <p>{product['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"View on Nykaa", key=f"nykaa_{product['id']}"):
                    st.success(f"Opening {product['name']} on Nykaa...")

def display_routine(data):
    """Display beauty routine"""
    routine = data.get('routine', {})
    
    if routine:
        st.markdown("### 📋 Your Personalized Routine")
        st.markdown(f"**{routine.get('title', 'Beauty Routine')}**")
        st.markdown(routine.get('description', ''))
        
        steps = routine.get('steps', [])
        for step in steps:
            st.markdown(f"""
            <div class="routine-step">
                <h4>Step {step.get('step', 1)}: {step.get('name', 'Step')}</h4>
                <p>{step.get('description', '')}</p>
                <p><em>Timing: {step.get('timing', 'As needed')}</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.info(f"⏰ **Total Time:** {routine.get('totalTime', 'Varies')}")
        st.info(f"🔄 **Frequency:** {routine.get('frequency', 'Daily')}")

def display_video_section(data):
    """Display video tutorial section"""
    st.markdown("### 🎥 Video Tutorial")
    
    if os.getenv('NOVELAI_API_KEY'):
        with st.spinner("Generating your personalized tutorial..."):
            # Simulate video generation
            st.info("🎬 Video generation would happen here with NovelAI Reel API")
            st.markdown("""
            **Tutorial Preview:**
            - Professional beauty demonstration
            - Step-by-step visual guide
            - 10-second focused content
            - No intro/outro - straight to the point
            """)
    else:
        st.warning("Video generation requires NovelAI API key. Here's a text tutorial instead:")
        st.markdown("""
        **Text Tutorial Steps:**
        1. Start with clean hands and face
        2. Apply products in thin, even layers
        3. Use gentle upward motions
        4. Allow each product to absorb
        5. Finish with sun protection (morning routine)
        """)

def handle_product_recommendations(data):
    """Handle product recommendation requests"""
    st.success("🛍️ Product recommendations added to chat!")

def handle_video_request(data):
    """Handle video tutorial requests"""
    st.success("🎥 Video tutorial section added to chat!")

def handle_routine_display(data):
    """Handle routine display"""
    st.success("📋 Personalized routine created!")

def analyze_skin_with_aws(image_data):
    """Analyze skin using AWS Rekognition"""
    if not st.session_state.aws_connected:
        return None, "AWS not connected"
    
    try:
        rekognition = st.session_state.aws_services.get('rekognition')
        if not rekognition:
            return None, "Rekognition service not available"
        
        # Analyze image for facial features and skin characteristics
        response = rekognition.detect_faces(
            Image={'Bytes': image_data},
            Attributes=['ALL']
        )
        
        # Process the response to extract skin-related insights
        insights = {
            'faces_detected': len(response['FaceDetails']),
            'analysis': 'Skin analysis completed using AWS Rekognition',
            'recommendations': [
                'Based on facial analysis, consider products for your skin type',
                'Regular skincare routine recommended',
                'Consult with dermatologist for specific concerns'
            ]
        }
        
        return insights, "Analysis completed successfully"
    except Exception as e:
        return None, f"Error analyzing image: {str(e)}"

def generate_voice_response(text):
    """Generate voice response using AWS Polly"""
    if not st.session_state.aws_connected:
        return None, "AWS not connected"
    
    try:
        polly = st.session_state.aws_services.get('polly')
        if not polly:
            return None, "Polly service not available"
        
        # Generate speech from text
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Joanna',  # Female voice suitable for beauty consultant
            Engine='neural'
        )
        
        return response['AudioStream'].read(), "Voice generated successfully"
    except Exception as e:
        return None, f"Error generating voice: {str(e)}"

def analyze_text_sentiment(text):
    """Analyze text sentiment using AWS Comprehend"""
    if not st.session_state.aws_connected:
        return None, "AWS not connected"
    
    try:
        comprehend = st.session_state.aws_services.get('comprehend')
        if not comprehend:
            return None, "Comprehend service not available"
        
        # Analyze sentiment
        response = comprehend.detect_sentiment(
            Text=text,
            LanguageCode='en'
        )
        
        return response, "Sentiment analysis completed"
    except Exception as e:
        return None, f"Error analyzing sentiment: {str(e)}"

def store_user_data_in_dynamodb(user_id, profile_data):
    """Store user profile data in DynamoDB"""
    if not st.session_state.aws_connected:
        return False, "AWS not connected"
    
    try:
        dynamodb = st.session_state.aws_services.get('dynamodb')
        if not dynamodb:
            return False, "DynamoDB service not available"
        
        # Assume we have a table called 'beauty-user-profiles'
        table = dynamodb.Table('beauty-user-profiles')
        
        # Store user profile
        table.put_item(
            Item={
                'user_id': user_id,
                'profile_data': profile_data,
                'timestamp': datetime.now().isoformat()
            }
        )
        
        return True, "Profile saved to cloud"
    except Exception as e:
        return False, f"Error saving profile: {str(e)}"

def reset_conversation():
    """Reset the conversation"""
    st.session_state.messages = []
    st.session_state.user_profile = {}
    st.session_state.conversation_step = 'greeting'
    st.session_state.session_id = str(uuid.uuid4())
    st.success("🔄 Conversation reset!")
    st.rerun()

def handle_user_input(user_input):
    """Handle user input and generate bot response"""
    # Add user message
    user_message = {
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now().isoformat()
    }
    st.session_state.messages.append(user_message)
    
    # Check for AWS-specific requests
    aws_response = None
    if st.session_state.aws_connected:
        if "analyze my skin" in user_input.lower() or "skin analysis" in user_input.lower():
            aws_response = handle_skin_analysis_request()
        elif "voice chat" in user_input.lower() or "voice mode" in user_input.lower():
            aws_response = handle_voice_chat_request()
        elif "save my profile" in user_input.lower():
            aws_response = handle_profile_save_request()
    
    # Generate bot response
    with st.spinner("Bella is thinking..."):
        try:
            # If AWS response is available, use it
            if aws_response:
                bot_message = aws_response
            else:
                # Create session data for the chatbot
                session_data = {
                    'userId': st.session_state.session_id,
                    'profile': st.session_state.user_profile,
                    'conversationHistory': st.session_state.messages,
                    'currentStep': st.session_state.conversation_step,
                    'preferences': {},
                    'aws_connected': st.session_state.aws_connected
                }
                
                # Analyze sentiment if AWS is connected
                if st.session_state.aws_connected:
                    sentiment_result, _ = analyze_text_sentiment(user_input)
                    if sentiment_result:
                        session_data['user_sentiment'] = sentiment_result['Sentiment']
                
                # Process message through chatbot
                response = asyncio.run(st.session_state.chatbot.process_message(user_input, session_data))
                
                # Update session state
                st.session_state.user_profile = session_data.get('profile', {})
                st.session_state.conversation_step = session_data.get('currentStep', 'general')
                
                # Add bot response
                bot_message = {
                    'role': 'assistant',
                    'content': response.get('message', 'I apologize, but I encountered an issue. Could you please try again?'),
                    'timestamp': datetime.now().isoformat(),
                    'type': response.get('type', 'text'),
                    'data': response.get('data', {}),
                    'suggestions': response.get('suggestions', [])
                }
            
            st.session_state.messages.append(bot_message)
            
            # Handle special response types
            if bot_message.get('type') == 'product_recommendations':
                handle_product_recommendations(bot_message.get('data', {}))
            elif bot_message.get('type') == 'video_tutorial_request':
                handle_video_request(bot_message.get('data', {}))
            elif bot_message.get('type') == 'routine_created':
                handle_routine_display(bot_message.get('data', {}))
            elif bot_message.get('type') == 'aws_skin_analysis':
                handle_aws_skin_analysis_display(bot_message.get('data', {}))
            
        except Exception as e:
            error_message = {
                'role': 'assistant',
                'content': f"I'm sorry, I encountered an error: {str(e)}. Please try again!",
                'timestamp': datetime.now().isoformat(),
                'type': 'error'
            }
            st.session_state.messages.append(error_message)
    
    st.rerun()

def handle_skin_analysis_request():
    """Handle skin analysis request using AWS"""
    return {
        'role': 'assistant',
        'content': "I'd love to help analyze your skin using AWS AI! Please upload a clear photo of your face, and I'll use AWS Rekognition to provide insights about your skin characteristics and recommend suitable products.",
        'timestamp': datetime.now().isoformat(),
        'type': 'aws_skin_analysis_request',
        'data': {'service': 'rekognition', 'feature': 'skin_analysis'}
    }

def handle_voice_chat_request():
    """Handle voice chat request using AWS Polly"""
    return {
        'role': 'assistant',
        'content': "Voice chat mode activated! I can now speak my responses using AWS Polly. My responses will include both text and audio. How can I help you with your beauty routine today?",
        'timestamp': datetime.now().isoformat(),
        'type': 'voice_chat_enabled',
        'data': {'service': 'polly', 'voice': 'Joanna'}
    }

def handle_profile_save_request():
    """Handle profile save request to DynamoDB"""
    success, message = store_user_data_in_dynamodb(
        st.session_state.session_id,
        st.session_state.user_profile
    )
    
    return {
        'role': 'assistant',
        'content': f"Profile save {'successful' if success else 'failed'}: {message}",
        'timestamp': datetime.now().isoformat(),
        'type': 'profile_save_result',
        'data': {'success': success, 'message': message}
    }

def handle_aws_skin_analysis_display(data):
    """Handle AWS skin analysis display"""
    st.success("🔬 AWS Skin Analysis completed!")

if __name__ == "__main__":
    main()
