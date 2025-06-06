@echo off
echo ========================================
echo    EchoLoop Automation System Startup
echo ========================================
echo.

echo 🔧 Checking system requirements...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

echo ✅ Python is available
echo.

echo 📦 Installing/updating dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

echo 🔑 Checking API configuration...
if not exist .env (
    echo ❌ .env file not found
    echo Creating .env file with your API keys...
    python create_env.py
)

echo ✅ API configuration ready
echo.

echo 🌐 Starting Web Monitor...
start "EchoLoop Web Monitor" python web_monitor.py

echo ⏳ Waiting for web server to start...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo    🚀 EchoLoop System Started!
echo ========================================
echo.
echo 📊 Web Monitor: http://localhost:5000
echo 🎮 Use the web interface to control automation
echo.
echo Available commands:
echo   - Start: Begin automation loop
echo   - Stop: Stop automation
echo   - Pause: Pause current operation
echo   - Resume: Resume paused operation
echo.
echo 📝 Logs are available in the web interface
echo 📁 Output files: ai_1_out.txt, ai_2_out.txt, ai_3_out.txt
echo.
echo Press any key to open web interface...
pause >nul

start http://localhost:5000

echo.
echo System is running! Close this window when done.
echo To stop the system, use the web interface or close all windows.
pause 