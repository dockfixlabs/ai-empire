@echo off
cd /d "%~dp0"

:: Kill old instances
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

:: Start Backend with hidden window
start "" /MIN pythonw.exe -c "import uvicorn, sys; sys.path.insert(0,'backend'); uvicorn.run('app.main:app', host='0.0.0.0', port=8000)"
echo [1/2] Backend started (PID: unknown - running hidden)

timeout /t 5 /nobreak >nul

:: Start Frontend with hidden window
start "" /MIN cmd /c "cd frontend && npm run dev -- --host 0.0.0.0 --port 5173"
echo [2/2] Frontend started

echo.
echo ========================================
echo  System is running 24/7
echo  Close this window - servers keep running
echo  To stop: run stop.bat
echo ========================================
echo  API:  http://localhost:8000
echo  Docs: http://localhost:8000/docs
echo  App:  http://localhost:5173
echo ========================================
