@echo off
setlocal

REM Set up environment paths for embedded Python
cd /d "%~dp0"

REM Set up paths relative to the resources folder
set PYTHONHOME=resources\python
set PYTHONPATH=resources\python
set PATH=resources\python;%PATH%

echo Launching ChatGPT Usage Analyzer...
resources\python\python.exe resources\analyze_usage.py
