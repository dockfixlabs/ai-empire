@echo off
cd /d "%~dp0"
echo ========================================
echo  Installing Auto-Start at Windows Boot
echo ========================================
echo.

:: Create scheduled task for backend
schtasks /create /tn "GumroadAI-Backend" /tr "pythonw.exe -c \"import uvicorn,sys; sys.path.insert(0,'%~dp0backend'); uvicorn.run('app.main:app',host='0.0.0.0',port=8000)\"" /sc onstart /delay 0000:30 /ru %USERNAME% /f
echo [1/2] Backend auto-start installed

:: Create scheduled task for frontend
schtasks /create /tn "GumroadAI-Frontend" /tr "cmd.exe /c cd /d \"%~dp0frontend\" && npm run dev -- --host 0.0.0.0 --port 5173" /sc onstart /delay 0001:00 /ru %USERNAME% /f
echo [2/2] Frontend auto-start installed

echo.
echo  Done! System will start automatically at boot.
echo  To remove: run remove-autostart.bat
echo.
pause
