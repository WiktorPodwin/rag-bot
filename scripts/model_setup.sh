set -e

export PYTHONPATH="$(pwd)/src"

echo "Downloading embedding model..."
python src/app/model_download.py
echo "Model downloaded successfully."