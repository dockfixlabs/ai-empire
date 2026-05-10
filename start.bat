@echo off
cd /d "%~dp0"
echo Starting servers...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.

cd backend
start /B python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 >nul 2>&1
echo [1/2] Backend started

cd ../frontend
start /B cmd /c "npm run dev -- --host 0.0.0.0 --port 5173" >nul 2>&1
echo [2/2] Frontend started

echo.
echo ========================================
echo  All servers running!
echo  API: http://localhost:8000/docs
echo  App: http://localhost:5173
echo ========================================
echo.
pause
