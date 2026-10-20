@echo off
REM YouTube Audio Ripper Launcher
REM Silent Windows launcher for YouTube Audio Ripper
setlocal

REM Resolve the application path from this script's own location.
set "APP_PATH=%~dp0"

REM Prefer a project-local virtualenv, then an environment override,
REM then a system Python on PATH.
set "PYTHON="
if exist "%APP_PATH%venv\Scripts\python.exe" set "PYTHON=%APP_PATH%venv\Scripts\python.exe"
if not defined PYTHON if defined HERMES_PYTHON set "PYTHON=%HERMES_PYTHON%"
if not defined PYTHON for %%P in (python.exe python) do if not defined PYTHON set "PYTHON=%%~$PATH:P"

if not defined PYTHON (
  echo [launcher] No Python interpreter found.
  echo [launcher] Create a virtualenv at "%APP_PATH%venv" or set HERMES_PYTHON.
  pause
  exit /b 1
)

REM Launch the application silently
start "" "%PYTHON%" "%APP_PATH%rip_gui.py"

echo YouTube Audio Ripper started.
endlocal
