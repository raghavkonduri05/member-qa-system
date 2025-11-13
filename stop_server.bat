@echo off
echo Stopping Q&A Server on port 8000...
echo.

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Found server process (PID: %%a)
    taskkill /F /PID %%a
    if errorlevel 1 (
        echo Failed to stop server
    ) else (
        echo Server stopped successfully!
    )
)

echo.
echo Checking if server is still running...
timeout /t 1 >nul
netstat -ano | findstr :8000 >nul
if errorlevel 1 (
    echo Server is stopped.
) else (
    echo Warning: Server may still be running. Try closing the command window manually.
)
echo.
pause



