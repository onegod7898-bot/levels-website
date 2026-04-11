@echo off
setlocal
cd /d "%~dp0"

echo.
echo  Levels — local preview
echo  Opening http://127.0.0.1:8765/ in your browser...
echo  Close the window titled "Levels preview server" when you are done.
echo.

start "Levels preview server" cmd /k "%~dp0_preview-server.cmd"

timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:8765/"

echo  If the page does not load, wait a second and refresh.
echo.
pause
