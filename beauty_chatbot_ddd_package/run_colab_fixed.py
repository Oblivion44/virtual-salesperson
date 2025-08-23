#!/usr/bin/env python3
"""
Beauty Chatbot DDD - Google Colab Execution Script (Fixed)
Complete implementation for running in Google Colab environment
"""

def setup_and_run_chatbot():
    """Main function to setup and run the chatbot in Colab"""
    
    # ============================================================================
    # PHASE 1: ENVIRONMENT SETUP
    # ============================================================================
    
    print("🌟 Beauty Recommendation Chatbot - DDD Enhanced")
    print("=" * 60)
    print("🚀 Starting Colab execution...")
    
    # Install packages
    print("\n🔧 Installing required packages...")
    import subprocess
    import sys
    
    packages = ['ipywidgets', 'pandas']
    for package in packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])
    
    # Import libraries
    import warnings
    warnings.filterwarnings('ignore')
    
    import os
    from pathlib import Path
    from datetime import datetime
    import random
    import json
    from typing import List, Dict, Optional
    from dataclasses import dataclass
    import uuid
    import ipywidgets as widgets
    from IPython.display import display, HTML, clear_output
    import pandas as pd
    import time
    
    print("✅ Environment setup complete!")
    
    # Clone repository
    print("\n📥 Cloning repository...")
    if not os.path.exists('/content/virtual-salesperson'):
        subprocess.run(['git', 'clone', 'https://github.com/Oblivion44/virtual-salesperson.git'], 
                       cwd='/content', check=True)
    
    os.chdir('/content/virtual-salesperson')
    print("✅ Repository ready!")
    
    # ============================================================================
    # PHASE 2: LOAD DDD COMPONENTS
    # ============================================================================
    
    print("\n🏗️ Loading DDD domain model...")
    
    # Add paths
    ddd_path = '/content/virtual-salesperson/beauty_chatbot_ddd_package/ddd_domain'
    core_path = '/content/virtual-salesperson/beauty_chatbot_ddd_package/core'
    sys.path.append(ddd_path)
    sys.path.append(core_path)
    
    try:
        # Import DDD components individually to avoid import * issues
        import value_objects
        import entities
        import aggregates
        import domain_services
        import repositories
        import domain_events
        import application_service
        import beauty_chatbot_simple
        
        print("✅ All DDD components loaded successfully!")
        
        # Create chatbot instance
        print("\n🤖 Initializing chatbot...")
        chatbot = beauty_chatbot_simple.create_chatbot()
        
        # Test basic functionality
        test_response = chatbot.process_message("Hello!")
        print(f"✅ Test response: {test_response['response'][:50]}...")
        
        # Test concern detection
        concern_response = chatbot.process_message("I have acne problems")
        print(f"✅ Concerns detected: {concern_response['concerns_detected']}")
        
        print("🎉 Chatbot initialization complete!")
        
    except Exception as e:
        print(f"❌ Error loading components: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    
    # ============================================================================
    # PHASE 3: DATA VALIDATION
    # ============================================================================
    
    print("\n📊 Validating data integration...")
    
    try:
        # Load sample data
        data_path = '/content/virtual-salesperson/beauty_chatbot_ddd_package/data'
        
        concerns_df = pd.read_csv(f'{data_path}/sample_concerns.csv')
        ingredients_df = pd.read_csv(f'{data_path}/sample_ingredients.csv')
        products_df = pd.read_csv(f'{data_path}/sample_products.csv')
        
        print(f"✅ Loaded {len(concerns_df)} concerns, {len(ingredients_df)} ingredients, {len(products_df)} products")
        
        # Test concern detection
        test_messages = [
            "I have acne problems",
            "My skin is very dry",
            "I need oily skin products"
        ]
        
        for message in test_messages:
            response = chatbot.process_message(message)
            print(f"✅ '{message}' -> {response['concerns_detected']}")
        
    except Exception as e:
        print(f"⚠️ Data loading issue: {str(e)}")
    
    # ============================================================================
    # PHASE 4: CREATE INTERACTIVE UI
    # ============================================================================
    
    print("\n🎨 Creating interactive chat interface...")
    
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
                widgets.HTML("<p>Ask me about skincare, haircare, or any beauty concerns!</p>"),
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
    
    # Create chat interface
    chat_interface = ColabChatInterface(chatbot)
    print("✅ Interactive chat interface created!")
    
    # ============================================================================
    # PHASE 5: TESTING
    # ============================================================================
    
    print("\n🧪 Running automated tests...")
    
    def run_tests():
        test_results = []
        
        # Test 1: Basic functionality
        try:
            response = chatbot.process_message("Hello")
            assert response['response'], "Response should not be empty"
            test_results.append("✅ Basic functionality: PASS")
        except Exception as e:
            test_results.append(f"❌ Basic functionality: FAIL - {str(e)}")
        
        # Test 2: Concern detection
        try:
            response = chatbot.process_message("I have acne problems")
            assert response['concerns_detected'], "Should detect acne concern"
            test_results.append("✅ Concern detection: PASS")
        except Exception as e:
            test_results.append(f"❌ Concern detection: FAIL - {str(e)}")
        
        # Test 3: Performance
        try:
            start_time = time.time()
            response = chatbot.process_message("My skin is dry")
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            assert response_time < 1000, "Response should be under 1 second"
            test_results.append(f"✅ Performance: PASS ({response_time:.0f}ms)")
        except Exception as e:
            test_results.append(f"❌ Performance: FAIL - {str(e)}")
        
        return test_results
    
    test_results = run_tests()
    for result in test_results:
        print(result)
    
    # ============================================================================
    # PHASE 6: DISPLAY INTERFACE
    # ============================================================================
    
    print("\n" + "="*60)
    print("🎉 Beauty Chatbot DDD successfully deployed in Colab!")
    print("💬 Ready to chat! Use the interface below to start conversations.")
    print("\n🔍 Try these sample messages:")
    print("   - 'I have acne problems'")
    print("   - 'My skin is very dry'") 
    print("   - 'Can you recommend products?'")
    print("   - 'Hello!'")
    print("="*60)
    
    # Display sample conversations guide
    display(HTML('''
    <div style="background-color: #e8f5e8; padding: 15px; border-radius: 10px; margin: 10px 0;">
        <h3>💡 Sample Conversations to Try</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 10px;">
            <div style="background: white; padding: 10px; border-radius: 5px;">
                <h4>🔍 Concern-Based</h4>
                <p><strong>Try:</strong> "I have acne problems"</p>
                <p><em>Get targeted advice and recommendations</em></p>
            </div>
            <div style="background: white; padding: 10px; border-radius: 5px;">
                <h4>🛒 Exploration</h4>
                <p><strong>Try:</strong> "Can you recommend skincare products?"</p>
                <p><em>Explore product categories and options</em></p>
            </div>
            <div style="background: white; padding: 10px; border-radius: 5px;">
                <h4>💬 General Chat</h4>
                <p><strong>Try:</strong> "Hello! How are you?"</p>
                <p><em>Friendly conversation and beauty tips</em></p>
            </div>
        </div>
    </div>
    '''))
    
    # Display the chat interface
    chat_interface.display()
    
    return chatbot, chat_interface

# Execute the setup
if __name__ == "__main__":
    chatbot, chat_interface = setup_and_run_chatbot()
else:
    # When called from exec(), run the setup
    chatbot, chat_interface = setup_and_run_chatbot()
