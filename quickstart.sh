#!/bin/bash
# UFO Sightings Dashboard - Quick Start Script
# Run this script to set up and start the project

echo "=================================="
echo "UFO Sightings Analytics Dashboard"
echo "Quick Start Setup"
echo "=================================="
echo ""

# Check Python version
echo "[1/5] Checking Python installation..."
python --version || { echo "Python not found! Please install Python 3.7+"; exit 1; }
echo "✓ Python is installed"
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
python -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate 2>/dev/null || venv\Scripts\activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "[4/5] Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run data loader
echo "[5/5] Loading dataset..."
echo ""
python data_loader.py
echo ""

echo "=================================="
echo "✓ Setup Complete!"
echo "=================================="
echo ""
echo "To start the Flask app, run:"
echo "  python app.py"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:5000"
echo ""
