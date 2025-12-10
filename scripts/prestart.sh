#!/bin/bash
set -e

# Add src/ to Python path
export PYTHONPATH=$(pwd)/src

# Run scripts
python src/app/connect_db.py
python src/app/init_db.py