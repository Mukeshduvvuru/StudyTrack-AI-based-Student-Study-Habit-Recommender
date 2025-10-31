@echo off
cls

echo ======================================
echo Study Habits Recommender System
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo Dependencies installed.
echo.

REM Create necessary directories
if not exist "models" mkdir models
if not exist "data" mkdir data
if not exist "uploads" mkdir uploads
echo Directories ready.
echo.

REM Run the application
echo ======================================
echo Starting Flask application...
echo ======================================
echo.
echo Access the application at:
echo 👉 http://localhost:5000
echo.
echo Admin credentials:
echo Username: admin
echo Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
pause
