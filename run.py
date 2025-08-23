#!/usr/bin/env python3
"""
Simple script to run the Beauty Chatbot Streamlit app
Perfect for running in Spyder or any Python environment
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import anthropic
        import requests
        import pandas
        import numpy
        import dotenv
        import textblob
        import aiohttp
        print("✅ All required packages are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Installing requirements...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Requirements installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install requirements")
            return False

def setup_environment():
    """Setup environment variables"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        env_file.write_text(env_example.read_text())
        print("⚠️  Please edit .env file with your API keys")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        if os.getenv('ANTHROPIC_API_KEY'):
            print("✅ Claude API key found")
        else:
            print("⚠️  Claude API key not found - running in demo mode")
        
        if os.getenv('NOVELAI_API_KEY'):
            print("✅ NovelAI API key found")
        else:
            print("ℹ️  NovelAI API key not found - text tutorials will be used")
            
    except ImportError:
        print("⚠️  python-dotenv not installed, skipping environment setup")

def run_streamlit():
    """Run the Streamlit app"""
    try:
        print("🚀 Starting Beauty Chatbot Streamlit App...")
        print("📱 The app will open in your default browser")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Beauty Chatbot stopped. Thanks for using Bella!")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")
        print("Try running manually: streamlit run app.py")

def main():
    """Main function"""
    print("🌟 Beauty Chatbot - Streamlit Version")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found. Please run this script from the project directory.")
        return
    
    # Check requirements
    if not check_requirements():
        return
    
    # Setup environment
    setup_environment()
    
    # Run the app
    run_streamlit()

if __name__ == "__main__":
    main()
