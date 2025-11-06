#!/bin/bash

# VLM Demo App - Quick Start Script

echo "🎨 Vision Language Model Demo - Starting up..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys before running."
    echo ""
    read -p "Press Enter to continue (make sure you've configured .env) or Ctrl+C to exit..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✨ Setup complete!"
echo ""
echo "🚀 Starting the application..."
echo "📍 The app will be available at: http://localhost:7860"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the app
python app.py
