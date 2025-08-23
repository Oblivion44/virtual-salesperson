#!/usr/bin/env python3
"""
Beauty Chatbot DDD - Google Colab Execution Script
Complete implementation for running in Google Colab environment
"""

# ============================================================================
# PHASE 1: ENVIRONMENT SETUP
# ============================================================================

def setup_environment():
    """Setup the Colab environment"""
    print("🔧 Setting up environment...")
    
    # Install packages
    import subprocess
    import sys
    
    packages = ['ipywidgets', 'pandas']
    for package in packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])
    
    # Import libraries
    import warnings
    warnings.filterwarnings('ignore')
    
    print("✅ Environment setup complete!")
    return True

def clone_repository():
    """Clone the repository"""
    print("📥 Cloning repository...")
    
    import subprocess
    import os
    
    # Clone repository
    subprocess.run(['git', 'clone', 'https://github.com/Oblivion44/virtual-salesperson.git'], 
                   cwd='/content', check=True)
    
    # Change to repository directory
    os.chdir('/content/virtual-salesperson')
    
    print("✅ Repository cloned successfully!")
    return True

# ============================================================================
# PHASE 2: DDD IMPLEMENTATION LOADING
# ============================================================================

def load_ddd_components():
    """Load all DDD domain components"""
    print("🏗️ Loading DDD domain model...")
    
    import sys
    from pathlib import Path
    
    # Add DDD domain to Python path
    ddd_path = '/content/virtual-salesperson/beauty_chatbot_ddd_package/ddd_domain'
    sys.path.append(ddd_path)
    
    try:
        # Import all DDD components
        from value_objects import *
        from entities import *
        from aggregates import *
        from domain_services import *
        from repositories import *
        from domain_events import *
        from application_service import *
        
        print("✅ DDD domain model loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading DDD components: {str(e)}")
        return False

def load_integration_layer():
    """Load the integration layer"""
    print("🔗 Loading integration components...")
    
    import sys
    
    # Add core integration layer to path
    core_path = '/content/virtual-salesperson/beauty_chatbot_ddd_package/core'
    sys.path.append(core_path)
    
    try:
        from beauty_chatbot_simple import SimplifiedBeautyChatbot, create_chatbot
        
        print("✅ Integration layer loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading integration layer: {str(e)}")
        return False

def initialize_chatbot():
    """Initialize the chatbot instance"""
    print("🤖 Initializing Beauty Chatbot...")
    
    try:
        from beauty_chatbot_simple import create_chatbot
        
        # Create chatbot instance
        chatbot = create_chatbot()
        
        # Test basic functionality
        test_response = chatbot.process_message("Hello!")
        print(f"✅ Test response: {test_response['response'][:50]}...")
        
        # Test concern detection
        concern_response = chatbot.process_message("I have acne problems")
        print(f"✅ Concerns detected: {concern_response['concerns_detected']}")
        
        print("🎉 Chatbot initialization complete!")
        return chatbot
        
    except Exception as e:
        print(f"❌ Chatbot initialization failed: {str(e)}")
        return None

# ============================================================================
# PHASE 3: DATA INTEGRATION
# ============================================================================

def load_sample_data():
    """Load and verify sample data"""
    print("📊 Loading sample CSV data...")
    
    import pandas as pd
    
    try:
        data_path = '/content/virtual-salesperson/beauty_chatbot_ddd_package/data'
        
        concerns_df = pd.read_csv(f'{data_path}/sample_concerns.csv')
        ingredients_df = pd.read_csv(f'{data_path}/sample_ingredients.csv')
        products_df = pd.read_csv(f'{data_path}/sample_products.csv')
        
        print(f"✅ Loaded {len(concerns_df)} concerns")
        print(f"✅ Loaded {len(ingredients_df)} ingredients") 
        print(f"✅ Loaded {len(products_df)} products")
        
        return {
            'concerns': concerns_df,
            'ingredients': ingredients_df,
            'products': products_df
        }
        
    except Exception as e:
        print(f"❌ Error loading sample data: {str(e)}")
        return None

def validate_data_integration(chatbot):
    """Validate data integration with concern detection"""
    print("🔍 Validating data integration...")
    
    test_messages = [
        "I have acne problems",
        "My skin is very dry",
        "I need oily skin products",
        "Can you help with aging?",
        "I have dark spots"
    ]
    
    results = []
    for message in test_messages:
        try:
            response = chatbot.process_message(message)
            results.append({
                'message': message,
                'concerns': response['concerns_detected'],
                'confidence': response['confidence_scores'],
                'type': response['prompt_type']
            })
        except Exception as e:
            results.append({
                'message': message,
                'error': str(e)
            })
    
    print("✅ Data integration validation complete!")
    return results

# ============================================================================
# PHASE 4: UI IMPLEMENTATION
# ============================================================================

def create_chat_interface(chatbot):
    """Create interactive chat interface for Colab"""
    print("🎨 Creating interactive chat interface...")
    
    import ipywidgets as widgets
    from IPython.display import display, clear_output, HTML
    from datetime import datetime
    
    class ColabChatInterface:
        def __init__(self, chatbot):
            self.chatbot = chatbot
            self.conversation_history = []
            self.setup_ui()
        
        def setup_ui(self):
            """Setup the chat interface"""
            # Chat display area
            self.chat_output = widgets.Output(layout={'height': '400px', 'overflow_y': 'auto'})
            
            # Input area
            self.message_input = widgets.Text(
                placeholder="Type your beauty question here...",
                layout={'width': '70%'}
            )
            
            # Send button
            self.send_button = widgets.Button(
                description="Send",
                button_style='primary',
                layout={'width': '15%'}
            )
            
            # Clear button
            self.clear_button = widgets.Button(
                description="Clear",
                button_style='warning',
                layout={'width': '15%'}
            )
            
            # Analytics display
            self.analytics_output = widgets.Output()
            
            # Event handlers
            self.send_button.on_click(self.send_message)
            self.clear_button.on_click(self.clear_chat)
            self.message_input.on_submit(self.send_message)
            
            # Layout
            input_box = widgets.HBox([self.message_input, self.send_button, self.clear_button])
            self.interface = widgets.VBox([
                widgets.HTML("<h2>🌟 Beauty Recommendation Chatbot - DDD Enhanced</h2>"),
                self.chat_output,
                input_box,
                widgets.HTML("<h3>📊 Analytics</h3>"),
                self.analytics_output
            ])
            
            # Initial welcome message
            self.display_message("Bot", "Hello! I'm your AI beauty expert. Ask me about skincare, haircare, or any beauty concerns!", "bot")
            self.update_analytics()
        
        def send_message(self, b=None):
            """Send user message and get bot response"""
            user_message = self.message_input.value.strip()
            if not user_message:
                return
            
            # Display user message
            self.display_message("You", user_message, "user")
            
            # Get bot response
            try:
                response = self.chatbot.process_message(user_message)
                self.display_message("Bot", response['response'], "bot")
                
                # Show additional info if available
                if response['concerns_detected']:
                    self.display_info(f"🔍 Concerns detected: {', '.join(response['concerns_detected'])}")
                
                if response['natural_remedies']:
                    self.display_info(f"🌿 Natural remedies available: {len(response['natural_remedies'])}")
                    
            except Exception as e:
                self.display_message("Bot", f"Sorry, I encountered an error: {str(e)}", "error")
            
            # Clear input and update analytics
            self.message_input.value = ""
            self.update_analytics()
        
        def display_message(self, sender, message, msg_type):
            """Display a message in the chat"""
            timestamp = datetime.now().strftime("%H:%M")
            
            if msg_type == "user":
                style = "background-color: #e3f2fd; margin: 5px 0; padding: 10px; border-radius: 10px; text-align: right;"
            elif msg_type == "bot":
                style = "background-color: #f3e5f5; margin: 5px 0; padding: 10px; border-radius: 10px;"
            else:
                style = "background-color: #ffebee; margin: 5px 0; padding: 10px; border-radius: 10px;"
            
            with self.chat_output:
                display(HTML(f'''
                    <div style="{style}">
                        <strong>{sender}</strong> <small>({timestamp})</small><br>
                        {message.replace(chr(10), "<br>")}
                    </div>
                '''))
        
        def display_info(self, info):
            """Display additional information"""
            with self.chat_output:
                display(HTML(f'''
                    <div style="background-color: #fff3e0; margin: 2px 0; padding: 5px; border-radius: 5px; font-size: 0.9em;">
                        {info}
                    </div>
                '''))
        
        def clear_chat(self, b=None):
            """Clear the chat history"""
            self.chat_output.clear_output()
            self.display_message("Bot", "Chat cleared! How can I help you with your beauty concerns?", "bot")
            self.update_analytics()
        
        def update_analytics(self):
            """Update analytics display"""
            try:
                analytics = self.chatbot.get_analytics()
                with self.analytics_output:
                    clear_output()
                    display(HTML(f'''
                        <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;">
                            📊 <strong>Conversations:</strong> {analytics.get('total_conversations', 0)} | 
                            💬 <strong>Messages:</strong> {analytics.get('total_messages', 0)} | 
                            🛒 <strong>Cart Items:</strong> {analytics.get('cart_items', 0)}
                        </div>
                    '''))
            except:
                pass
        
        def display(self):
            """Display the interface"""
            display(self.interface)
    
    # Create and return the interface
    chat_interface = ColabChatInterface(chatbot)
    print("✅ Interactive chat interface created!")
    return chat_interface

# ============================================================================
# PHASE 5: TESTING & VALIDATION
# ============================================================================

def run_automated_tests(chatbot):
    """Run comprehensive automated tests"""
    print("🧪 Running Automated Test Suite...")
    print("=" * 50)
    
    test_results = []
    
    # Test 1: Basic functionality
    try:
        response = chatbot.process_message("Hello")
        assert response['response'], "Response should not be empty"
        test_results.append(("✅", "Basic functionality", "PASS"))
    except Exception as e:
        test_results.append(("❌", "Basic functionality", f"FAIL: {str(e)}"))
    
    # Test 2: Concern detection
    try:
        response = chatbot.process_message("I have acne problems")
        assert response['concerns_detected'], "Should detect acne concern"
        test_results.append(("✅", "Concern detection", "PASS"))
    except Exception as e:
        test_results.append(("❌", "Concern detection", f"FAIL: {str(e)}"))
    
    # Test 3: Analytics
    try:
        analytics = chatbot.get_analytics()
        assert isinstance(analytics, dict), "Analytics should return dict"
        test_results.append(("✅", "Analytics system", "PASS"))
    except Exception as e:
        test_results.append(("❌", "Analytics system", f"FAIL: {str(e)}"))
    
    # Test 4: Cart functionality
    try:
        chatbot.add_to_cart({"name": "Test Product", "price": 25.99})
        cart = chatbot.get_cart()
        assert len(cart) > 0, "Cart should have items"
        test_results.append(("✅", "Cart functionality", "PASS"))
    except Exception as e:
        test_results.append(("❌", "Cart functionality", f"FAIL: {str(e)}"))
    
    # Display results
    print("\n📊 Test Results:")
    for status, test_name, result in test_results:
        print(f"{status} {test_name}: {result}")
    
    passed = sum(1 for _, _, result in test_results if result == "PASS")
    total = len(test_results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    return passed == total

def run_performance_tests(chatbot):
    """Test response times and performance"""
    print("⚡ Running Performance Tests...")
    print("=" * 40)
    
    import time
    
    test_messages = [
        "I have acne problems",
        "My skin is dry and flaky", 
        "Can you recommend products?",
        "What's good for oily skin?",
        "Hello there!"
    ]
    
    response_times = []
    
    for message in test_messages:
        start_time = time.time()
        response = chatbot.process_message(message)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        response_times.append(response_time)
        
        print(f"Message: '{message[:30]}...'")
        print(f"Response time: {response_time:.2f}ms")
        print("---")
    
    avg_response_time = sum(response_times) / len(response_times)
    max_response_time = max(response_times)
    
    print(f"\n📊 Performance Summary:")
    print(f"Average response time: {avg_response_time:.2f}ms")
    print(f"Maximum response time: {max_response_time:.2f}ms")
    print(f"Target: < 500ms ({'✅ PASS' if avg_response_time < 500 else '⚠️ SLOW'})")
    
    return avg_response_time < 500

# ============================================================================
# MAIN EXECUTION FUNCTION
# ============================================================================

def main():
    """Main execution function for Colab"""
    print("🌟 Beauty Recommendation Chatbot - DDD Enhanced")
    print("=" * 60)
    print("🚀 Starting Colab execution...")
    
    try:
        # Phase 1: Environment Setup
        print("\n" + "="*20 + " PHASE 1: ENVIRONMENT SETUP " + "="*20)
        setup_environment()
        clone_repository()
        
        # Phase 2: Code Deployment
        print("\n" + "="*20 + " PHASE 2: CODE DEPLOYMENT " + "="*20)
        if not load_ddd_components():
            raise Exception("Failed to load DDD components")
        
        if not load_integration_layer():
            raise Exception("Failed to load integration layer")
        
        chatbot = initialize_chatbot()
        if not chatbot:
            raise Exception("Failed to initialize chatbot")
        
        # Phase 3: Data Integration
        print("\n" + "="*20 + " PHASE 3: DATA INTEGRATION " + "="*20)
        sample_data = load_sample_data()
        if sample_data:
            validation_results = validate_data_integration(chatbot)
            print(f"✅ Validated {len(validation_results)} test cases")
        
        # Phase 4: UI Implementation
        print("\n" + "="*20 + " PHASE 4: UI IMPLEMENTATION " + "="*20)
        chat_interface = create_chat_interface(chatbot)
        
        # Phase 5: Testing & Validation
        print("\n" + "="*20 + " PHASE 5: TESTING & VALIDATION " + "="*20)
        tests_passed = run_automated_tests(chatbot)
        performance_ok = run_performance_tests(chatbot)
        
        # Final Results
        print("\n" + "="*20 + " EXECUTION COMPLETE " + "="*20)
        print("🎉 Beauty Chatbot DDD successfully deployed in Colab!")
        print(f"✅ Tests passed: {tests_passed}")
        print(f"✅ Performance OK: {performance_ok}")
        print("\n💬 Ready to chat! Use the interface above to start conversations.")
        
        # Display the chat interface
        print("\n🎨 Displaying chat interface...")
        chat_interface.display()
        
        return chatbot, chat_interface
        
    except Exception as e:
        print(f"\n❌ Execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

# ============================================================================
# COLAB EXECUTION
# ============================================================================

if __name__ == "__main__":
    # This will be executed when the script is run in Colab
    chatbot, chat_interface = main()
    
    if chatbot and chat_interface:
        print("\n" + "="*60)
        print("🌟 SUCCESS! Your Beauty Chatbot is ready!")
        print("💬 Start chatting using the interface above")
        print("🔍 Try messages like:")
        print("   - 'I have acne problems'")
        print("   - 'My skin is very dry'") 
        print("   - 'Can you recommend products?'")
        print("   - 'Hello!'")
        print("="*60)
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
