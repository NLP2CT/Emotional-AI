@echo off
echo Stopping all related services...

:: Kill all Python processes (if multiple services are using Python)
taskkill /F /IM python.exe /T

:: Optional: If you want to ensure specific processes are stopped, you can also target specific scripts or services
:: taskkill /F /IM "realtime.py" /T
:: taskkill /F /IM "webui.py" /T

echo All related services have been stopped.
pause
