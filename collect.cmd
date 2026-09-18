@echo off
cd /d "%~dp0"
py -3 -m sysinfo_collector --copy 2>nul
if errorlevel 1 python -m sysinfo_collector --copy
pause