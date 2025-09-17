@echo off
echo =====================================
echo GitHub Upload Helper for Python Files
echo =====================================
echo.

echo Step 1: Install Git (if not installed)
echo - Download from: https://git-scm.com/
echo - Install with default settings
echo - Restart this script after installation
echo.
pause

echo Step 2: Initialize Git Repository
git init
if errorlevel 1 (
    echo Error: Git not found! Please install Git first.
    pause
    exit /b 1
)

echo Step 3: Create .gitignore (already done)
echo Python files and folders to ignore are configured

echo Step 4: Add Python files to Git
git add *.py
git add requirements.txt
git add README.md
git add .gitignore
git add start.bat
git add index.html

echo Step 5: Check what will be committed
git status

echo.
echo Step 6: Commit changes
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Initial Python incident management system

git commit -m "%commit_msg%"

echo.
echo Step 7: Manual GitHub steps
echo =============================
echo 1. Go to https://github.com/new
echo 2. Repository name: incident-response-system-python
echo 3. Description: AI-Enhanced Incident Response System in Python
echo 4. Choose Public or Private
echo 5. Do NOT initialize with README (we already have one)
echo 6. Click "Create repository"
echo.
echo 7. Copy the repository URL and paste it here:
set /p repo_url="https://github.com/ingenious222/incident-response-system "

echo Step 8: Add remote and push
git branch -M main
git remote add origin %repo_url%
git push -u origin main

echo.
echo ==========================================
echo SUCCESS! Your Python project is on GitHub
echo ==========================================
echo.
echo Repository URL: %repo_url%
echo.
echo Files uploaded:
echo - ai_processor.py     (AI analysis module)
echo - app.py             (Flask web server)
echo - project.py         (Command line interface)
echo - run.py             (Launcher script)
echo - requirements.txt   (Dependencies)
echo - README.md          (Documentation)
echo - .gitignore         (Git ignore rules)
echo - test_app.py        (Test suite)
echo - status_check.py    (Health check)
echo - start.bat          (Windows launcher)
echo - index.html         (Web interface)
echo.
pause