@echo off
cd /d "%~dp0"
title Levels preview server
echo Serving: %CD%
echo URL: http://127.0.0.1:8765/
echo Close this window to stop the server.
echo.
python -m http.server 8765 --bind 127.0.0.1
if errorlevel 1 (
  echo.
  echo Python failed. Install Python or run: npm install ^&^& npm run preview
  pause
)
