@echo off
title Rockstar Games Services - Launcher Builder

echo [INFO] Starting build process...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] PyInstaller not found. Installing...
    python -m pip install pyinstaller
    echo.
)

if not exist launcher.py (
    echo [ERROR] launcher.py not found in the current directory.
    pause
    exit /b 1
)

set ICON_ARG=
if exist icon.ico (
    set ICON_ARG=--icon=icon.ico
) else (
    echo [WARNING] icon.ico not found. Building without custom icon.
)

set DATA_ARG=
if exist media (
    set DATA_ARG=--add-data "media;media"
) else (
    echo [WARNING] media folder not found. Building without video assets.
)

echo [INFO] Compiling launcher...
echo.

python -m PyInstaller --noconsole --onefile --name rockstar_games_services_launcher_gta_sa %ICON_ARG% %DATA_ARG% launcher.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed. Check the output above for details.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Build completed successfully.
echo [INFO] Executable location: dist\rockstar_games_services_launcher_gta_sa.exe
echo.
pause
