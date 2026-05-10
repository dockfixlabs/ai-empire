@echo off
echo Stopping all servers...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul
echo All servers stopped.
pause
