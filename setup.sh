BASE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MICROSERVICES=(
    ms-productos
    ms-ventas
    ms-pagos
    ms-auth
    ms-register
    ms-mail
    ms-token
    ms-despacho
    ms-img
    ms-orchestrator
    frontend
)

for MICROSERVICE in "${MICROSERVICES[@]}"
do
    echo "Procesando $MICROSERVICE..."

    cd "$BASE_PATH/$MICROSERVICE" || { echo "No se pudo acceder a $MICROSERVICE"; exit 1; }

    if [ ! -d "venv" ]; then
        echo "Creando entorno virtual..."
        python3 -m venv venv
    else
        echo "El entorno virtual ya existe en $MICROSERVICE/venv"
    fi

    source venv/bin/activate

    if [ -f "requirements.txt" ]; then
        echo "Instalando dependencias..."
        pip install -r requirements.txt
    else
        echo "No se encontró requirements.txt en $MICROSERVICE."
    fi

    deactivate

    cd "$BASE_PATH" || exit

    echo "Proceso completado para $MICROSERVICE."
    echo "----------------------------------------"
done

echo "Todos los entornos virtuales han sido configurados."
