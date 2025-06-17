# Ferremas
Trabajo Integración de plataformas 010V

## Base de datos

En MySQL se deben cargar los 2 archivos de la carpeta SQL.

```
Ferremas.sql
comunas.sql
```

## .env
Se debe generar un archivo **.env** con los datos adjuntos en la entrega.

## Instalación servidor

### Automatizada

Se debe ejecutar el siguiete archivo <br>

```powershell
setup.bat
```
Este archivo se encarga de crear el entorno virtual e instalar las librerias necesarias en cada microservicio

Una vez instalado, para ejecutar ejecutar los microservicios, se debe ejecutar el siguiente archivo
```powershell
run_ms.bat
```
Este archivo se encarga de ejecutar todos los servicios correspondientes.

### Manual
Por cada uno de los microservicios (Incluyendo frontend) se debe de generar un entorno virtual

```powershell
python -m venv venv 
python\scripts\venv
```
Una vez el entorno virtual este activo, se deben de instalar las librerias

```powershell
pip install -r requirements.txt
```

Con el entorno virtual activo y las librerias instaladas, ahora solo falta ejecutar el servicios

```powershell
python app.py
```

## Puertos

| nombre ms  | puerto   |
|------------|----------|
|ms-producto |   5000   |
|ms-ventas   |   5001   |
|ms-pagos    |   5002   |
|ms-Auth     |   5003   |
|ms-register |   5004   |
|ms-mail     |   5005   |
|ms-token    |   5006   |
|ms-despacho |   5007   |
|ms-img      |   5008   |