@echo off
setlocal enabledelayedexpansion

:: --- VENV MANAGER ---
echo Checking Virtual Environment...

if defined VIRTUAL_ENV (
    echo [OK] Virtual Environment already active: %VIRTUAL_ENV%
    goto config
)

if exist "venv\Scripts\activate.bat" (
    echo [OK] Activating existing Virtual Environment...
    call venv\Scripts\activate.bat
    goto config
)

echo [WARN] Virtual Environment NOT found!
set /p create_venv="Would you like to create it and install requirements? (y/n): "

if /I "!create_venv!"=="y" (
    echo [WAIT] Creating Virtual Environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo [WAIT] Installing requirements...
    pip install --upgrade pip
    pip install -r requirements.txt
    echo [OK] Environment ready.
) else (
    echo [!] Proceeding with system Python (NOT recommended).
    set /p confirm="Are you sure? (y/n): "
    if /I "!confirm!" NEQ "y" exit /b
)

:config
:: --- CONFIGURATION ---
set "CLI_NAME=markitdown-cli"
set "GUI_NAME=launcher"

:: --- CHECK UPX ---
:: Linearizzato senza parentesi per evitare errori con il punto "."
set "UPX_CMD="
if exist "upx.exe" set "UPX_CMD=--upx-dir=."
if exist "upx.exe" (echo [OK] UPX found. Compression enabled.) else (echo [INFO] UPX not found. Proceeding without compression.)

:: Check parameters
if "%1"=="" goto build_all
if /I "%1"=="cli" goto build_cli
if /I "%1"=="gui" goto build_gui

echo Invalid parameter: %1
echo Usage: build.bat [cli ^| gui] or run without parameters for both.
pause
exit /b

:build_all
call :build_cli
call :build_gui
goto end

:build_cli
echo.
echo --------------------------------------------------
echo [1] Compiling CLI Engine...
echo --------------------------------------------------
pyinstaller --onefile --console --clean ^
 --collect-data magika ^
 %UPX_CMD% ^
 --exclude-module customtkinter ^
 --exclude-module darkdetect ^
 --exclude-module tkinterdnd2 ^
 --name %CLI_NAME% ^
 markitdown-cli.py
if /I "%1"=="cli" goto end
exit /b

:build_gui
echo.
echo --------------------------------------------------
echo [2] Compiling GUI Launcher...
echo --------------------------------------------------
pyinstaller --onefile --noconsole --clean ^
 --collect-all tkinterdnd2 ^
 %UPX_CMD% ^
 --exclude-module markitdown ^
 --exclude-module numpy ^
 --exclude-module pandas ^
 --exclude-module onnxruntime ^
 --name %GUI_NAME% ^
 launcher.py
exit /b

:end
echo.
echo --------------------------------------------------
echo Cleaning temporary folders and spec files...
if exist build rmdir /s /q build
if exist *.spec del /f /q *.spec
echo --------------------------------------------------
echo Done! Executables are in: dist/
echo --------------------------------------------------
pause