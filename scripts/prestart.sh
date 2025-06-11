set -x
set -e

# Starts DB connection
python src/app/connect_db.py

# Initializes data in DB
python src/app/init_db.py