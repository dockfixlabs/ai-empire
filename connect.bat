@echo off
chcp 65001 >nul
echo ============================================================
echo    Gumroad AI Empire - Connection Helper
echo ============================================================
echo.
echo الخطوة 1: افتح https://app.gumroad.com/settings/advanced
echo الخطوة 2: في قسم API، انقر "Generate access token"
echo الخطوة 3: انسخ التوكن الذي يظهر
echo.
set /p TOKEN="الصق التوكن هنا: "
echo.
echo جاري الربط...
curl -s -X POST "http://localhost:8000/api/v1/auth/login" -H "Content-Type: application/json" -d "{\"email\":\"admin@gumroad.ai\",\"password\":\"YOUR_PASSWORD\"}" > login.json
for /f "tokens=2 delims=:,}" %%a in ('type login.json ^| find "access_token"') do set TOK=%%~a
echo.
del login.json
