# Beauty Chatbot DDD - One Cell Colab Execution
# Copy and paste this entire cell into Google Colab

# Install packages
import subprocess
import sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ipywidgets', 'pandas', '-q'])

# Import libraries
import os
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import pandas as pd

print("🌟 Beauty Recommendation Chatbot - DDD Enhanced")
print("=" * 60)

# Clone repository
if not os.path.exists('/content/virtual-salesperson'):
    print("📥 Cloning repository...")
    subprocess.run(['git', 'clone', 'https://github.com/Oblivion44/virtual-salesperson.git'], cwd='/content')
    print("✅ Repository cloned!")

os.chdir('/content/virtual-salesperson')

# Add paths
sys.path.append('/content/virtual-salesperson/beauty_chatbot_ddd_package/ddd_domain')
sys.path.append('/content/virtual-salesperson/beauty_chatbot_ddd_package/core')

# Import components
print("🏗️ Loading DDD components...")
try:
    import beauty_chatbot_simple
    chatbot = beauty_chatbot_simple.create_chatbot()
    print("✅ Chatbot initialized!")
    
    # Test
    test_response = chatbot.process_message("Hello!")
    print(f"✅ Test: {test_response['response'][:30]}...")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")

# Create simple chat interface
print("🎨 Creating chat interface...")

class SimpleChatInterface:
    def __init__(self, chatbot):
        self.chatbot = chatbot
        
        # Create widgets
        self.chat_output = widgets.Output(layout={'height': '350px', 'overflow_y': 'auto'})
        self.message_input = widgets.Text(placeholder="Ask about beauty concerns...", layout={'width': '75%'})
        self.send_button = widgets.Button(description="Send", button_style='primary', layout={'width': '25%'})
        
        # Event handlers
        self.send_button.on_click(self.send_message)
        self.message_input.on_submit(self.send_message)
        
        # Layout
        input_box = widgets.HBox([self.message_input, self.send_button])
        self.interface = widgets.VBox([
            widgets.HTML("<h2>🌟 Beauty AI Expert - Ready to Help!</h2>"),
            self.chat_output,
            input_box
        ])
        
        # Welcome message
        with self.chat_output:
            display(HTML('''
                <div style="background-color: #f3e5f5; padding: 10px; border-radius: 10px; margin: 5px 0;">
                    <strong>Bot</strong><br>
                    Hello! I'm your AI beauty expert. Ask me about:
                    <ul>
                        <li>🔍 Skin concerns (acne, dryness, oily skin, aging)</li>
                        <li>💄 Product recommendations</li>
                        <li>🌿 Natural remedies</li>
                        <li>📚 Beauty education</li>
                    </ul>
                    Try: "I have acne problems" or "My skin is very dry"
                </div>
            '''))
    
    def send_message(self, b=None):
        user_message = self.message_input.value.strip()
        if not user_message:
            return
        
        # Display user message
        with self.chat_output:
            display(HTML(f'''
                <div style="background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin: 5px 0; text-align: right;">
                    <strong>You</strong><br>{user_message}
                </div>
            '''))
        
        # Get bot response
        try:
            response = self.chatbot.process_message(user_message)
            bot_message = response['response']
            
            # Display bot response
            with self.chat_output:
                display(HTML(f'''
                    <div style="background-color: #f3e5f5; padding: 10px; border-radius: 10px; margin: 5px 0;">
                        <strong>Bot</strong><br>{bot_message.replace(chr(10), "<br>")}
                    </div>
                '''))
                
                # Show detected concerns
                if response['concerns_detected']:
                    display(HTML(f'''
                        <div style="background-color: #fff3e0; padding: 5px; border-radius: 5px; margin: 2px 0; font-size: 0.9em;">
                            🔍 Detected: {", ".join(response['concerns_detected'])}
                        </div>
                    '''))
                
                # Show natural remedies info
                if response['natural_remedies']:
                    display(HTML(f'''
                        <div style="background-color: #e8f5e8; padding: 5px; border-radius: 5px; margin: 2px 0; font-size: 0.9em;">
                            🌿 Natural remedies available: {len(response['natural_remedies'])}
                        </div>
                    '''))
        
        except Exception as e:
            with self.chat_output:
                display(HTML(f'''
                    <div style="background-color: #ffebee; padding: 10px; border-radius: 10px; margin: 5px 0;">
                        <strong>Bot</strong><br>Sorry, I encountered an error: {str(e)}
                    </div>
                '''))
        
        # Clear input
        self.message_input.value = ""
    
    def show(self):
        display(self.interface)

# Create and display interface
chat_interface = SimpleChatInterface(chatbot)

print("🎉 Setup complete! Chat interface ready below:")
print("💬 Try messages like:")
print("   - 'I have acne problems'")
print("   - 'My skin is very dry'")
print("   - 'Can you recommend products?'")
print("="*60)

chat_interface.show()
