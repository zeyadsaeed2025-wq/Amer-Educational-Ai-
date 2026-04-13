@echo off
title EduForge AI - Starting Services
echo ========================================
echo Starting EduForge AI Services...
echo ========================================

echo.
echo [1] Starting Backend on port 10000...
cd /d "%~dp0backend"
start "EduForge Backend" cmd /k "python -m uvicorn main:app --host 127.0.0.1 --port 10000"

timeout /t 4 /nobreak > nul

echo [2] Starting Frontend on port 5173...
cd /d "%~dp0frontend\dist"
start "EduForge Frontend" cmd /k "python -m http.server 5173"

timeout /t 2 /nobreak > nul

echo.
echo ========================================
echo Services Started!
echo.
echo Backend API:   http://127.0.0.1:10000
echo Frontend UI:   http://127.0.0.1:5173
echo.
echo Open http://127.0.0.1:5173 in your browser!
echo ========================================
pause