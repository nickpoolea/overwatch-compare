@echo off
echo Starting Overwatch Comparison App...
echo.

REM Get the directory of this batch file
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo Error: Virtual environment not found at .venv\Scripts\python.exe
    echo Please make sure your Python virtual environment is set up correctly.
    pause
    exit /b 1
)

REM Start the launcher
echo Running the Python launcher...
".venv\Scripts\python.exe" start_app.py

pause
