@echo off
echo Installing Python dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Dependencies installed successfully!
    echo Starting Interview Bot...
    echo.
    python interview_bot/chat_interface.py
) else (
    echo.
    echo Error installing dependencies.
    echo Please make sure Python is installed and added to PATH.
    echo.
    pause
)