@echo off
REM This script is used to run the Windows version of the game.
cd ..

REM Activate the virtual environment
call .venv\Scripts\activate

REM Run the game
pythonw.exe main.py

REM Deactivate the virtual environment
deactivate