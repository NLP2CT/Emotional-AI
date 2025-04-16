@echo off
setlocal ENABLEDELAYEDEXPANSION

:: Conda Python version
set "PYTHON_VER=3.10"

:: User control (true to show command windows, false for background)
set SHOW_CMD=true  :: Set to false to run in the background

:: Option to control waiting for launch_panel.bat completion
set WAIT_FOR_LAUNCH_PANEL=true  :: Set to true if you want to wait for launch_panel.bat to complete

:: ==========================================================
:: Log initialization
:: ==========================================================
set ROOT_DIR=%~dp0
set LOG_FILE=%ROOT_DIR%multi_env_log.txt
echo ============================== > %LOG_FILE%
echo [START] Multi-service initialization log [%DATE% %TIME%] >> %LOG_FILE%
echo ============================== >> %LOG_FILE%

:: ==========================================================
:: Start GPT-SoVITS inference service
:: ==========================================================
echo Starting GPT-SoVITS inference service...
echo [INFO] Starting GPT-SoVITS inference service... [%TIME%]

if "%WAIT_FOR_LAUNCH_PANEL%"=="true" (
    echo [INFO] Waiting for launch_panel.bat to complete... [%TIME%]
    call "%ROOT_DIR%launch_panel.bat" >> %LOG_FILE% 2>&1
) else (
    echo [INFO] Not waiting for launch_panel.bat, moving to next service... [%TIME%]
    start "" cmd /k "%ROOT_DIR%launch_panel.bat" >> %LOG_FILE% 2>&1
)

:: If needed, record the result of calling the script and check errorlevel
if errorlevel 1 (
    echo [ERROR] GPT-SoVITS inference service failed to start [%DATE% %TIME%] >> %LOG_FILE%
    pause
    exit /b
) else (
    echo [SUCCESS] GPT-SoVITS inference service started successfully [%DATE% %TIME%] >> %LOG_FILE%
)
pause

:: ==========================================================
:: Start SenseVoice WebUI (using Conda)
:: ==========================================================
set "SV_NAME=SenseVoice-main"
set "SV_ENV=env_%SV_NAME%"
set "SV_SCRIPT=webui.py"
set "SV_DIR=%ROOT_DIR%%SV_NAME%"
set "SV_REQUIRE=%SV_DIR%\requirements.txt"

:: Get conda base path
for /f "delims=" %%A in ('conda info --base') do set "CONDA_BASE=%%A"
set "SV_PYTHON=%CONDA_BASE%\envs\%SV_ENV%\python.exe"
set "SV_PIP=%CONDA_BASE%\envs\%SV_ENV%\Scripts\pip.exe"

echo.
echo ==============================
echo [SenseVoice WebUI] Starting...
echo ==============================
echo [INFO] Starting SenseVoice WebUI... [%TIME%]
start "" cmd /k "call conda activate %SV_ENV% && cd /d %SV_DIR% && python %SV_SCRIPT%"

:: If needed, create the conda environment
conda env list | findstr /C:"%SV_ENV%" >nul
if !ERRORLEVEL! NEQ 0 (
    echo - Creating environment %SV_ENV%
    echo [INFO] Creating environment %SV_ENV%... >> %LOG_FILE%
    call conda create -y -n %SV_ENV% python=%PYTHON_VER% >> %LOG_FILE% 2>&1
)

:: Install requirements from the requirements file
if exist "%SV_REQUIRE%" (
    echo [INFO] Installing requirements from %SV_REQUIRE%... >> %LOG_FILE%
    "%SV_PIP%" install -r "%SV_REQUIRE%" >> %LOG_FILE% 2>&1
)

:: Check if the script exists and launch the web UI
if exist "%SV_DIR%\%SV_SCRIPT%" (
    echo - Launching SenseVoice WebUI...
    echo [INFO] Launching SenseVoice WebUI... [%TIME%] >> %LOG_FILE%
) else (
    echo [ERROR] %SV_SCRIPT% not found in %SV_NAME% >> %LOG_FILE%
    echo [ERROR] %SV_SCRIPT% not found. >> %LOG_FILE%
)

pause


:: ==========================================================
:: Start other Conda services 
:: ==========================================================
set SERVICES=gptsovits-r-solution microphone
set SCRIPT_gptsovits-r-solution=realtime.py
set SCRIPT_microphone=call.py

for %%P in (%SERVICES%) do (
    set "ENV_NAME=env_%%P"
    set "SERVICE_DIR=%ROOT_DIR%%%P"
    set "REQUIRE_FILE=!SERVICE_DIR!\requirements.txt"
    set "RUN_SCRIPT=!SCRIPT_%%P!"
    set "ENV_PYTHON=%CONDA_BASE%\envs\!ENV_NAME!\python.exe"
    set "ENV_PIP=%CONDA_BASE%\envs\!ENV_NAME!\Scripts\pip.exe"

    echo.
    echo ==============================
    echo [Service] %%P
    echo ==============================
    echo [INFO] Starting service %%P... [%TIME%]
    start "" cmd /k "call conda activate !ENV_NAME! && cd /d !SERVICE_DIR! && python !RUN_SCRIPT!"

    conda env list | findstr /C:"!ENV_NAME!" >nul
    if !ERRORLEVEL! NEQ 0 (
        echo [INFO] Creating conda env "!ENV_NAME!"... >> %LOG_FILE%
        call conda create -y -n !ENV_NAME! python=%PYTHON_VER% >> %LOG_FILE% 2>&1
    )

    if exist "!REQUIRE_FILE!" (
        echo [INFO] Installing requirements from !REQUIRE_FILE!... >> %LOG_FILE%
        "!ENV_PIP!" install -r "!REQUIRE_FILE!" >> %LOG_FILE% 2>&1
    )

    if exist "!SERVICE_DIR!\!RUN_SCRIPT!" (
        echo - Launching !RUN_SCRIPT!...
        echo [INFO] Launching !RUN_SCRIPT!... [%TIME%] >> %LOG_FILE%
    ) else (
        echo [ERROR] Script !RUN_SCRIPT! not found in %%P. >> %LOG_FILE%
    )

    echo ------------------------------ >> %LOG_FILE%
)

pause
:: ==========================================================
:: Completion
:: ==========================================================
echo.
echo All services initialized.
echo [INFO] All services initialized. [%TIME%] >> %LOG_FILE%
echo [COMPLETE] %DATE% %TIME% >> %LOG_FILE%
echo Log saved to: %LOG_FILE%
pause
