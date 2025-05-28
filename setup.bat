@echo off
SETLOCAL

:: Definir la lista de microservicios
set MICRO1=ms-ventas
set MICRO2=ms-productos
set MICRO3=ms-pagos
set MICRO4=ms-auth


:: Función para crear y configurar el entorno virtual
call :setup_venv %MICRO1%
call :setup_venv %MICRO2%
call :setup_venv %MICRO3%
call :setup_venv %MICRO4%

echo Todos los entornos virtuales han sido configurados.
goto :eof

:: Subrutina para crear y configurar el entorno virtual en un microservicio
:setup_venv
set MICROSERVICE=%1
echo Creando entorno virtual en %MICROSERVICE%...

:: Ir al directorio del microservicio
cd C:\Users\plazavespucio\ferramas\%MICROSERVICE%

:: Verificar si el directorio venv existe. Si no, crear el entorno virtual.
IF NOT EXIST venv (
    echo Creando entorno virtual...
    python -m venv venv
) ELSE (
    echo El entorno virtual ya existe en %MICROSERVICE%\venv
)

:: Activar el entorno virtual
call venv\Scripts\activate.bat

:: Instalar las dependencias si existe el archivo requirements.txt
IF EXIST requirements.txt (
    echo Instalando dependencias...
    pip install -r requirements.txt
) ELSE (
    echo No se encontró requirements.txt en %MICROSERVICE%.
)

:: Desactivar el entorno virtual
deactivate

echo Proceso completado para %MICROSERVICE%.
goto :eof