@echo off
setlocal
cd /d "%~dp0"

echo Checking for Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo Python was not found on your computer.
    echo Please install Python 3.10 or newer from https://www.python.org/downloads/
    echo IMPORTANT: Check the box that says "Add python.exe to PATH" during installation.
    echo.
    pause
    exit /b 1
)

if not exist ".venv" (
    echo Creating a local app environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

call ".venv\Scripts\activate.bat"

echo Installing or updating required packages...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo.
    echo Could not install required packages. Check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

if not exist ".env" if exist ".env.example" (
    copy ".env.example" ".env" >nul
)

echo Opening your browser app...
streamlit run app.py

pause