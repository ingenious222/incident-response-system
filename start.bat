@echo off
echo Starting AI-Enhanced Incident Response System (Python Version)
echo.
echo Choose an option:
echo 1. Start Web Server (Flask)
echo 2. Start Command Line Interface
echo 3. Exit
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Starting Flask web server on http://127.0.0.1:4506
    echo Press Ctrl+C to stop the server
    echo.
    E:\proj\secod\.venv\Scripts\python.exe app.py
) else if "%choice%"=="2" (
    echo Starting Command Line Interface
    echo.
    E:\proj\secod\.venv\Scripts\python.exe project.py
) else if "%choice%"=="3" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice!
    pause
)

pause