
cd "$(dirname "$0")/frontend" || exit 1

source venv/bin/activate

python app.py

read -p "Presiona Enter para salir..."