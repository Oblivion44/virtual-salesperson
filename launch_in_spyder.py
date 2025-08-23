"""
Beauty Chatbot - Spyder Launch Script
=====================================

This script is specifically designed to run the Beauty Chatbot in Spyder IDE.
Simply run this file in Spyder and the Streamlit app will launch in your browser.

Instructions for Spyder:
1. Open this file in Spyder
2. Run the entire script (F5)
3. The app will open in your default browser
4. Use Ctrl+C in Spyder console to stop the server

Author: Beauty Chatbot Team
Version: 1.0.0
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print("🌟 BEAUTY CHATBOT - STREAMLIT VERSION")
    print("=" * 60)
    print("✨ AI-Powered Virtual Beauty Consultant")
    print("🤖 Powered by Claude 3.5 & NovelAI Reel")
    print("🎯 Strand Agents Architecture")
    print("=" * 60)

def check_spyder_environment():
    """Check if running in Spyder"""
    try:
        # Check for Spyder-specific variables
        if 'SPYDER_ARGS' in os.environ or 'SPY_PYTHONPATH' in os.environ:
            print("✅ Running in Spyder IDE")
            return True
        else:
            print("ℹ️  Not detected as Spyder (but that's okay!)")
            return False
    except:
        return False

def install_requirements():
    """Install required packages"""
    print("\n📦 Checking and installing requirements...")
    
    required_packages = [
        'streamlit==1.28.1',
        'anthropic==0.7.8',
        'requests==2.31.0',
        'pandas==2.1.3',
        'python-dotenv==1.0.0',
        'textblob==0.17.1',
        'aiohttp==3.9.1'
    ]
    
    for package in required_packages:
        try:
            package_name = package.split('==')[0]
            __import__(package_name.replace('-', '_'))
            print(f"✅ {package_name} already installed")
        except ImportError:
            print(f"📥 Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package_name} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                return False
    
    return True

def setup_environment():
    """Setup environment variables and files"""
    print("\n🔧 Setting up environment...")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📝 Creating .env file from template...")
            env_file.write_text(env_example.read_text())
        else:
            print("📝 Creating basic .env file...")
            env_content = """# API Keys (Optional - app works in demo mode without them)
ANTHROPIC_API_KEY=your_claude_api_key_here
NOVELAI_API_KEY=your_novelai_api_key_here

# Nykaa Integration (Optional)
NYKAA_AFFILIATE_ID=your_affiliate_id

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
"""
            env_file.write_text(env_content)
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        if os.getenv('ANTHROPIC_API_KEY') and os.getenv('ANTHROPIC_API_KEY') != 'your_claude_api_key_here':
            print("✅ Claude API key configured")
        else:
            print("⚠️  Claude API key not configured - running in demo mode")
        
        if os.getenv('NOVELAI_API_KEY') and os.getenv('NOVELAI_API_KEY') != 'your_novelai_api_key_here':
            print("✅ NovelAI API key configured")
        else:
            print("ℹ️  NovelAI API key not configured - text tutorials will be used")
            
    except ImportError:
        print("⚠️  python-dotenv not available")

def launch_streamlit():
    """Launch the Streamlit application"""
    print("\n🚀 Launching Beauty Chatbot...")
    print("📱 The app will open in your default browser")
    print("🔗 URL: http://localhost:8501")
    print("🛑 Use Ctrl+C in Spyder console to stop the server")
    print("-" * 60)
    
    try:
        # Change to the correct directory
        os.chdir(current_dir)
        
        # Launch Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--server.headless", "true"
        ]
        
        # Start the process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Open browser
        webbrowser.open("http://localhost:8501")
        
        print("✅ Streamlit server started successfully!")
        print("💬 Start chatting with Bella, your AI beauty consultant!")
        print("\nFeatures available:")
        print("  🌿 Skincare recommendations")
        print("  💇‍♀️ Hair care advice") 
        print("  💄 Makeup suggestions")
        print("  📋 Personalized routines")
        print("  🎥 Video tutorials (with API key)")
        print("\n" + "=" * 60)
        
        # Keep the process running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n👋 Stopping Beauty Chatbot...")
            process.terminate()
            process.wait()
            print("✅ Server stopped successfully!")
            
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the correct directory")
        print("2. Try running: pip install streamlit")
        print("3. Try running manually: streamlit run app.py")

def main():
    """Main function to run everything"""
    print_banner()
    
    # Check environment
    check_spyder_environment()
    
    # Verify we have the app file
    if not Path("app.py").exists():
        print("❌ app.py not found!")
        print("Please make sure you're running this script from the beauty-chatbot-streamlit directory")
        return
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements. Please install manually.")
        return
    
    # Setup environment
    setup_environment()
    
    # Launch the app
    launch_streamlit()

# Run the application
if __name__ == "__main__":
    main()

# For Spyder users: You can also run individual parts by selecting and pressing F9
# Or run the entire script with F5

"""
SPYDER USAGE INSTRUCTIONS:
=========================

Method 1 - Run Entire Script:
1. Open this file in Spyder
2. Press F5 to run the entire script
3. The app will launch in your browser

Method 2 - Run in Console:
1. In Spyder console, navigate to the project directory:
   cd /path/to/beauty-chatbot-streamlit
2. Run: exec(open('launch_in_spyder.py').read())

Method 3 - Manual Launch:
1. In Spyder console: !pip install streamlit
2. In Spyder console: !streamlit run app.py

The app will be available at: http://localhost:8501
"""
