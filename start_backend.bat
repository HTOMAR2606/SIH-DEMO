@echo off
echo ========================================================
echo    PM Internship Allocation Engine - Backend API
echo ========================================================
echo.
echo Starting the backend API server...
echo This will make the API accessible from any device on your network.
echo.
echo Press Ctrl+C to stop the server
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Start the API server
python recommendation_api.py

echo.
echo Backend API server stopped.
pause
