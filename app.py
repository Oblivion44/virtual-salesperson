import streamlit as st
import asyncio
import json
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

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

def main():
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>✨ Bella - AI Beauty Consultant</h1>
        <p>Your personal beauty expert powered by AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status indicator
    api_status = "🟢 Connected" if os.getenv('ANTHROPIC_API_KEY') else "🟡 Demo Mode"
    st.markdown(f'<div class="status-indicator">{api_status}</div>', unsafe_allow_html=True)
    
    # Sidebar for user profile and controls
    with st.sidebar:
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
        
        # Display suggestions
        suggestions = message.get('suggestions', [])
        if suggestions:
            display_suggestions(suggestions)

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

def reset_conversation():
    """Reset the conversation"""
    st.session_state.messages = []
    st.session_state.user_profile = {}
    st.session_state.conversation_step = 'greeting'
    st.session_state.session_id = str(uuid.uuid4())
    st.success("🔄 Conversation reset!")
    st.rerun()

if __name__ == "__main__":
    main()
