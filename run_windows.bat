@echo off
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (
  python app.py
) else (
  py app.py
)
if errorlevel 1 (
  echo.
  echo The application did not start. Check that Python 3 is installed and available.
  pause
)
