@echo off
REM IPL Predictor - Quick Start Script for Windows

echo 🏏 IPL Predictor - Setting up project...

REM Backend Setup
echo 📦 Setting up backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ✅ Backend dependencies installed

REM Create .env file
if not exist ".env" (
    copy .env.example .env
    echo ✅ .env file created (please edit with your settings)
)

cd ..

REM Frontend Setup
echo 📦 Setting up frontend...
cd frontend

REM Install dependencies
call npm install
echo ✅ Frontend dependencies installed

REM Create .env file
if not exist ".env" (
    copy .env.example .env
    echo ✅ Frontend .env file created
)

cd ..

echo.
echo ✅ Setup complete!
echo.
echo 📋 Next steps:
echo 1. Edit backend\.env with your database and Redis settings
echo 2. Edit frontend\.env with your API URL
echo 3. Start PostgreSQL and Redis
echo 4. Run: start.bat (or see README.md for manual instructions)
echo.
echo 🚀 To start the application:
echo    Backend:  cd backend ^&^& venv\Scripts\activate.bat ^&^& python app/main.py
echo    Frontend: cd frontend ^&^& npm start
