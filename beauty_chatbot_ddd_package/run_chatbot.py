#!/usr/bin/env python3
"""
Beauty Recommendation Chatbot - DDD Enhanced Version
Main runner script for the deployed chatbot
"""

import sys
import os
from pathlib import Path

# Add paths
sys.path.append(str(Path(__file__).parent / "ddd_domain"))
sys.path.append(str(Path(__file__).parent / "core"))

# Import the simplified chatbot
from beauty_chatbot_simple import create_chatbot

def main():
    """Main function to run the chatbot"""
    print("🌟 Beauty Recommendation Chatbot - DDD Enhanced")
    print("=" * 50)
    print("Welcome to your AI Beauty Expert! 💄✨")
    print()
    
    try:
        # Create chatbot instance
        print("🚀 Initializing chatbot...")
        chatbot = create_chatbot()
        print("✅ Chatbot ready!")
        print()
        
        # Interactive chat loop
        print("💬 Start chatting! (type 'quit' to exit)")
        print("-" * 30)
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Thanks for using Beauty Chatbot! Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Process message
            response = chatbot.process_message(user_input)
            
            print(f"Bot: {response['response']}")
            
            if response['concerns_detected']:
                print(f"🔍 Concerns detected: {', '.join(response['concerns_detected'])}")
            
            if response['natural_remedies']:
                print(f"🌿 Natural remedies available: {len(response['natural_remedies'])}")
            
            print()
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
