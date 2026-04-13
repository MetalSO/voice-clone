@echo off
chcp 65001 >nul
title Voice Service - Frontend

echo ========================================
echo   Voice Service - Frontend Starter
echo ========================================
echo.

cd /d "d:\trea speech synthesis\voice-input-frontend"

echo [1/2] Checking Node.js environment...
node --version
echo.

echo [2/2] Starting Vue dev server...
echo ----------------------------------------------
echo Frontend: http://localhost:5173
echo ----------------------------------------------
echo Press Ctrl+C to stop
echo.

npm run dev

pause
