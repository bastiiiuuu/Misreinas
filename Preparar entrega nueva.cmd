@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 goto :error
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error
".venv\Scripts\python.exe" manage.py migrate --noinput
if errorlevel 1 goto :error
".venv\Scripts\python.exe" manage.py preparar_demo
if errorlevel 1 goto :error
echo.
echo Preparacion completa. Abre Iniciar Mis Reinas.cmd para ver el sitio.
goto :end
:error
echo No se pudo preparar el proyecto. Revisa el mensaje anterior.
:end
pause
endlocal
