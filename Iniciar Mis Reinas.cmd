@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 goto :error
)
".venv\Scripts\python.exe" -c "import django, PIL, tzdata" >nul 2>&1
if errorlevel 1 (
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto :error
)
".venv\Scripts\python.exe" manage.py migrate --noinput
if errorlevel 1 goto :error
echo.
echo Mis Reinas: http://127.0.0.1:8001/
echo Administrador: http://127.0.0.1:8001/admin/
echo Para detener el servidor, presiona Ctrl+C.
".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8001
goto :end
:error
echo.
echo No se pudo iniciar. Revisa el mensaje anterior y las instrucciones de README.md.
:end
pause
endlocal
