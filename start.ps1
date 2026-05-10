# Gumroad AI Empire - Startup Script
Write-Host "🚀 Starting Gumroad AI Empire..." -ForegroundColor Cyan

# Start Backend
$backend = Start-Job -ScriptBlock {
    $env:Path += ";C:\Users\PC\AppData\Local\Python\pythoncore-3.14-64\Scripts"
    Set-Location "C:\Users\PC\gumroad\backend"
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Wait for backend to start
Start-Sleep -Seconds 4

Write-Host "✅ Backend running at http://localhost:8000" -ForegroundColor Green
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Yellow

# Start Frontend
$frontend = Start-Job -ScriptBlock {
    Set-Location "C:\Users\PC\gumroad\frontend"
    npm run dev
}

Start-Sleep -Seconds 3

Write-Host "✅ Frontend running at http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Dashboard: http://localhost:5173" -ForegroundColor Cyan
Write-Host "📚 API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Red

# Keep script running
try {
    while ($true) {
        Start-Sleep -Seconds 10
        Write-Host "   [System Running] $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor DarkGray
    }
} finally {
    Stop-Job $backend
    Stop-Job $frontend
    Remove-Job $backend
    Remove-Job $frontend
}
