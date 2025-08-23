#!/bin/bash

# Beauty Chatbot Web App Startup Script
echo "🌟 Starting Beauty Chatbot Web App Setup..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm are available"

# Create required directories
echo "📁 Creating required directories..."
mkdir -p public/videos
mkdir -p public/images
mkdir -p logs

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys before running the app"
    echo "   Required: ANTHROPIC_API_KEY, NOVELAI_API_KEY"
fi

# Create placeholder images
echo "🖼️  Creating placeholder images..."
if [ ! -f public/images/placeholder-product.jpg ]; then
    # Create a simple placeholder (you can replace this with actual image)
    echo "Creating placeholder product image..."
fi

# Check if API keys are configured
if grep -q "your_.*_key_here" .env; then
    echo "⚠️  WARNING: Please configure your API keys in .env file"
    echo "   ANTHROPIC_API_KEY=your_claude_api_key_here"
    echo "   NOVELAI_API_KEY=your_novelai_api_key_here"
    echo ""
    echo "🔑 Get your API keys from:"
    echo "   - Anthropic Claude: https://console.anthropic.com/"
    echo "   - NovelAI: https://novelai.net/"
    echo ""
    read -p "Press Enter to continue anyway (app will use fallback features)..."
fi

# Start the application
echo "🚀 Starting Beauty Chatbot Web App..."
echo "📱 The app will be available at: http://localhost:3000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start with development mode if available, otherwise production
if command -v nodemon &> /dev/null; then
    echo "🔄 Starting in development mode with auto-reload..."
    npm run dev
else
    echo "▶️  Starting in production mode..."
    npm start
fi
