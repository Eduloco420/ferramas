@echo off
SETLOCAL

set BASE_PATH=%~dp0

set MICRO1=ms-ventas
set MICRO2=ms-productos
set MICRO3=ms-pagos
set MICRO4=ms-auth

call :setup_venv %MICRO1%
call :setup_venv %MICRO2%
call :setup_venv %MICRO3%
call :setup_venv %MICRO4%

echo Todos los entornos virtuales han sido configurados.
goto :eof

:setup_venv
set MICROSERVICE=%1
echo Creando entorno virtual en %MICROSERVICE%...

pushd "%BASE_PATH%\%MICROSERVICE%"

IF NOT EXIST venv (
    echo Creando entorno virtual...
    python -m venv venv
) ELSE (
    echo El entorno virtual ya existe en %MICROSERVICE%\venv
)

call venv\Scripts\activate

IF EXIST requirements.txt (
    echo Instalando dependencias...
    pip install -r requirements.txt
) ELSE (
    echo No se encontró requirements.txt en %MICROSERVICE%.
)

deactivate

popd
echo Proceso completado para %MICROSERVICE%.
goto :eof
