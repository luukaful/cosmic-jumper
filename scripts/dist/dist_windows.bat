@echo off
REM Step 1: Build the project into an .exe using pyinstaller
pyinstaller --onefile --noconsole main.py

REM Step 2: Create a new folder for the build output
set OUTPUT_DIR=build_output
if not exist %OUTPUT_DIR% mkdir %OUTPUT_DIR%

REM Step 3: Move the .exe file into the new folder
move dist\main.exe %OUTPUT_DIR%\

REM Step 4: Copy the assets folder into the new folder
xcopy assets %OUTPUT_DIR%\assets /E /I /Y

REM Step 5: Clean up unnecessary build files
rmdir /S /Q build
rmdir /S /Q dist
del main.spec

if exist %OUTPUT_DIR%\main.exe echo Build process completed successfully!
pause