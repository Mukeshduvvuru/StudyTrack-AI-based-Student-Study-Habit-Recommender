#!/bin/bash

# Study Habits Recommender - Run Script

echo "======================================"
echo "Study Habits Recommender System"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "Error: Could not find activation script"
    exit 1
fi
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "Dependencies installed."
echo ""

# Create necessary directories
mkdir -p models data uploads static/css static/js templates
echo "Directories ready."
echo ""

# Run the application
echo "======================================"
echo "Starting Flask application..."
echo "======================================"
echo ""
echo "Access the application at:"
echo "👉 http://localhost:5000"
echo ""
echo "Admin credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
