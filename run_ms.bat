@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

echo Iniciando todos los microservicios en nuevas ventanas...

for /D %%D in (ms-*) do (
    echo Ejecutando %%D...
    start "%%D" cmd /k "cd /d %%~fD && call venv\Scripts\activate.bat && python app.py"
)

echo Todos los microservicios han sido lanzados.
