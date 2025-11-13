@echo off
echo Checking for existing server on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Stopping existing server (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
    timeout /t 1 >nul
)

echo.
echo Starting server...
echo Note: API key is loaded from .env file automatically
echo.
echo ========================================
echo Server will be available at:
echo   Web Interface: http://localhost:8000/
echo   API Docs:      http://localhost:8000/docs
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.
python main.py
pause

