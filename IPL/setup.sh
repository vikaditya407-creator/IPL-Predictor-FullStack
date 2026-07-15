#!/bin/bash

# IPL Predictor - Quick Start Script

set -e

echo "🏏 IPL Predictor - Setting up project..."

# Backend Setup
echo "📦 Setting up backend..."
cd backend

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Backend dependencies installed"

# Create .env file from .env.example
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ .env file created (please edit with your settings)"
fi

cd ..

# Frontend Setup
echo "📦 Setting up frontend..."
cd frontend

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

# Install dependencies
npm install
echo "✅ Frontend dependencies installed"

# Create .env file
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Frontend .env file created"
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit backend/.env with your database and Redis settings"
echo "2. Edit frontend/.env with your API URL"
echo "3. Start PostgreSQL and Redis"
echo "4. Run: ./start.sh (or see README.md for manual instructions)"
echo ""
echo "🚀 To start the application:"
echo "   Backend:  cd backend && source venv/bin/activate && python app/main.py"
echo "   Frontend: cd frontend && npm start"
