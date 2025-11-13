# PowerShell script to start the server
# Note: API key is loaded from .env file automatically
Write-Host "Starting server..." -ForegroundColor Green
Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Web Interface: http://localhost:8000/" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Note: Make sure you have created a .env file with your OPENAI_API_KEY" -ForegroundColor Yellow
Write-Host ""
python main.py



