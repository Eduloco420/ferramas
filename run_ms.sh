BASE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Iniciando todos los microservicios en background..."

# Recorrer todos los subdirectorios que comienzan con 'ms-'
for dir in "$BASE_PATH"/ms-*/; do
    # Obtener solo el nombre de la carpeta
    service=$(basename "$dir")
    
    echo "Ejecutando $service..."
    
    (
        cd "$dir" || exit 1
        source venv/bin/activate
        python app.py
    ) &

done

echo "Todos los microservicios han sido lanzados en background."
