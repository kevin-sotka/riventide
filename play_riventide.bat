@echo off
REM Riventide Launcher for Windows

REM Change to the directory of this script
cd /d "%~dp0"

REM Check if we have a virtual environment
if exist .venv (
    REM Activate the virtual environment and run the game
    call .venv\Scripts\activate.bat
    python main.py
) else (
    REM Run with system Python
    python main.py
)

REM Pause if there was an error
if %ERRORLEVEL% neq 0 (
    echo.
    echo An error occurred while running Riventide.
    pause
) 