@echo off
echo ========================================================
echo    PM Internship Allocation Engine - Frontend
echo ========================================================
echo.
echo Starting the frontend web server...
echo This will serve the web application on your network.
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

REM Navigate to frontend directory
cd /d "%~dp0frontend"

REM Start the web server
echo Starting web server on http://192.168.0.119:8080
echo.
echo Access from any device on your network:
echo   📱 Mobile/Tablet: http://192.168.0.119:8080
echo   💻 Computer:      http://192.168.0.119:8080
echo   🏠 Local:         http://localhost:8080
echo.

python -m http.server 8080 --bind 0.0.0.0

echo.
echo Frontend web server stopped.
pause
