@echo off
chcp 65001 >nul
title Voice Service - Backend

echo ========================================
echo   Voice Service - Backend Starter
echo ========================================
echo.

cd /d "d:\trea speech synthesis"

echo [1/5] Checking Python environment...
"d:\trea speech synthesis\venv\Scripts\python.exe" --version
echo.

echo [2/5] Checking port 8080 availability...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do (
    echo Port 8080 is in use by PID %%a, stopping process...
    taskkill /F /PID %%a >nul 2>&1
)
echo Port 8080 is now available.
echo.

echo [3/5] Setting environment variables...
set "PATH=C:\Users\Administrator\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin;%PATH%"
set "FFMPEG_PATH=C:\Users\Administrator\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"
echo FFmpeg path configured.
echo.

echo [4/5] Installing required packages if needed...
"d:\trea speech synthesis\venv\Scripts\python.exe" -m pip install --upgrade pip --quiet 2>nul
"d:\trea speech synthesis\venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet 2>nul
echo.

echo [5/5] Starting FastAPI service...
echo ----------------------------------------------
echo Service: http://localhost:8080
echo API Docs: http://localhost:8080/docs
echo ----------------------------------------------
echo Press Ctrl+C to stop
echo.

"d:\trea speech synthesis\venv\Scripts\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8080

pause
