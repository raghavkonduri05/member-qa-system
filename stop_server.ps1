# PowerShell script to stop the server
Write-Host "Stopping Q&A Server on port 8000..." -ForegroundColor Yellow
Write-Host ""

$processes = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique

if ($processes) {
    foreach ($pid in $processes) {
        $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
        if ($proc) {
            Write-Host "Stopping process: $($proc.ProcessName) (PID: $pid)" -ForegroundColor Cyan
            Stop-Process -Id $pid -Force
            Write-Host "Server stopped successfully!" -ForegroundColor Green
        }
    }
} else {
    Write-Host "No server found running on port 8000." -ForegroundColor Green
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")



